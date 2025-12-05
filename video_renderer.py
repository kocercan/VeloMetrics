#!/usr/bin/env python3
# ================================================================
#  ANA VIDEO RENDER MODÜLÜ (video_renderer.py)
#  ================================================================
#  PRO VERSİYON v5 - MODÜLER YAPISAL
#
#  Temel işlevler:
#  - Video dosyasından frame'ler oku
#  - GPX verilerini frame zamanına göre interpolasyon yap
#  - Tüm widget'ları çiz
#  - Çıkış video dosyasına yaz
#
#  CURVED SCREEN EFEKTİ KALDIRILDI
#  - İçbükey widget arka planları var (cascade efekti)
#  - Konveks video distorsiyon yok
#  ================================================================

import cv2
import numpy as np
from datetime import timedelta
from moviepy import VideoFileClip, VideoClip
from tqdm import tqdm
import math
import sys
import os
import shutil
import tempfile

# Modülleri import et
from config import (
    GPX_DOSYASI, VIDEO_DOSYASI, CIKTI_DOSYASI, ZAMAN_OFFSET_SANIYE,
    DEMO_MODU, KONVEKS_EFEKT, İÇBÜKEY_EFEKT,
    DEMO_MODE_SECONDS, DEMO_START_SECONDS,
    WIDGET_WIDTH_RATIO, WIDGET_HEIGHT_RATIO, WIDGET_MIN_WIDTH, WIDGET_MIN_HEIGHT,
    BOX_SIZE_RATIO, BOX_SIZE_MIN, PADDING_RATIO, PADDING_MIN, GAP_RATIO, GAP_MIN,
    PROGRESS_BAR_WIDTH_RATIO, PROGRESS_BAR_HEIGHT,
    QUALITY_CONFIG, HUD_CONFIG
)
from data_handler import DataHandler, get_hr_zone
from utils import clear_gradient_cache, draw_power_icon
from hud_layout import render_unified_hud
from config import COLORS, WIDGETS_ENABLED
from widgets import draw_panel_v2


# ================================================================
#  BAŞLANGIÇ VE DOĞRULAMA
#  ================================================================

def validate_and_prepare():
    """
    Validate required files and load VideoFileClip.
    """
    print("\n" + "="*60)
    print("  PRO VERSION v5 - MODULAR RENDER")
    print("="*60)
    
    try:
        print(f"\n📹 Loading video file: {VIDEO_DOSYASI}")
        clip = VideoFileClip(VIDEO_DOSYASI)
        print(f"   ✅ {int(clip.duration)}s, {clip.fps} fps, {int(clip.size[0])}x{int(clip.size[1])}")
    except (OSError, FileNotFoundError):
        print(f"❌ ERROR: '{VIDEO_DOSYASI}' not found!")
        sys.exit(1)
    
    print(f"\n📍 Loading GPX file: {GPX_DOSYASI}")
    try:
        data_handler = DataHandler(GPX_DOSYASI)
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)
    
    print(f"\n⏱️  Time offset: {ZAMAN_OFFSET_SANIYE} seconds")
    if DEMO_MODU:
        print(f"🎬 Demo mode: ON (first {DEMO_MODE_SECONDS}s)")
    else:
        print("🎬 Demo mode: OFF (full video)")
    print(f"📺 Effects:")
    print(f"   • Concave widget background: {'ON' if İÇBÜKEY_EFEKT else 'OFF'}")
    print(f"   • Convex video distortion: {'ON' if KONVEKS_EFEKT else 'OFF'}")
    
    return clip, data_handler


def ensure_output_writable(output_path):
    """
    Quick check whether we can create a file in the directory containing
    `output_path`. If not writable, print actionable container run commands
    and exit so the user can re-run with correct mount/UID flags.
    """
    out_dir = os.path.dirname(os.path.abspath(output_path)) or '.'
    test_file = os.path.join(out_dir, '.vpro_write_test')
    try:
        with open(test_file, 'wb') as f:
            f.write(b'v')
        os.remove(test_file)
        return True
    except Exception as e:
        print(f"\n❌ Write permission test failed: {e}")
        print("   • Cannot write to target directory from container.")
        print("   • Solution (podman):")
        print("       podman run --rm -v \"$(pwd):/app:rw,z\" --userns=keep-id video-proje python3 video_renderer.py")
        print("     (':z' fixes SELinux labels, '--userns=keep-id' maps UID)")
        print("   • Solution (docker):")
        print("       docker run --rm -u $(id -u):$(id -g) -v \"$(pwd):/app:rw\" video-proje python3 video_renderer.py")
        print("     (maps user ID to allow container to write on mount)")
        print("   • Alternative: run container as root (security risk):")
        print("       docker run --rm -u 0 -v \"$(pwd):/app:rw\" video-proje python3 video_renderer.py")
        print("\n   • If these commands don't work, check host-side mount folder permissions.")
        return False


def precompute_resources(W, H):
    """
    Precompute resources for rendering.
    
    - Warm up gradient cache
    - Create test gradients
    """
    print("\n🔥 Precomputing resources...")
    
    # Calculate widget dimensions (test)
    bw_test = max(int(W * WIDGET_WIDTH_RATIO), WIDGET_MIN_WIDTH)
    bh_test = max(int(H * WIDGET_HEIGHT_RATIO), WIDGET_MIN_HEIGHT)
    box_test = max(int(min(W, H) * BOX_SIZE_RATIO), BOX_SIZE_MIN)
    
    # Warm up gradient cache
    if QUALITY_CONFIG['precompute_gradients']:
        from utils import create_concave_gradient
        print(f"   • Widget gradient: {bw_test}x{bh_test}")
        _ = create_concave_gradient(bw_test, bh_test)
        print(f"   • Large box gradient: {box_test}x{box_test}")
        _ = create_concave_gradient(box_test, box_test)
        print("   ✅ Gradient cache created")


# ================================================================
#  FRAME RENDER LOOP
#  ================================================================

def render_video(clip, data_handler, output_file):
    """
    Render video and write to output file.
    
    Args:
        clip: MoviePy VideoFileClip object
        data_handler: DataHandler object
        output_file: Output video file
    """
    W, H = int(clip.size[0]), int(clip.size[1])
    
    # Limit video duration in demo mode
    duration = clip.duration
    # Demo start offset handling
    start_offset = 0.0
    if DEMO_MODU:
        start_offset = float(DEMO_START_SECONDS)
        # Avoid starting beyond clip duration
        if start_offset >= duration:
            print(f"❌ DEMO_START_SECONDS ({start_offset}s) >= clip duration ({duration}s); resetting to 0")
            start_offset = 0.0
        duration = min(float(DEMO_MODE_SECONDS), max(0.0, duration - start_offset))
        print(f"\n🎬 Processing {int(duration)}s in demo mode (start: {int(start_offset)}s)")
    
    # Use MoviePy to render MP4 via ffmpeg (libx264). This avoids cv2 VideoWriter
    # codec issues inside Docker and produces H.264 MP4 output.
    fps = clip.fps
    print(f"\n📝 Opening output video:")
    print(f"   • File: {output_file}")
    print(f"   • Resolution: {W}x{H}")
    print(f"   • FPS: {fps}")
    print(f"   • Codec: libx264 (MP4)")

    print("\n▶️  Starting render...\n")

    # Cache for HUD rendering to allow lower update rates (improves perf)
    hud_cache = {'t': -9999.0, 'bgr': None, 'alpha': None}

    # make_frame must return an RGB image (H, W, 3) as float [0..255] or uint8
    def make_frame(t_sec):
        # Map local timeline t_sec to source clip time if demo start offset is used
        src_t = t_sec + start_offset if DEMO_MODU else t_sec

        # Get source frame (RGB)
        frame_rgb = clip.get_frame(src_t)

        # Convert to BGR for OpenCV-based HUD rendering
        img_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        # Interpolate GPX data for this source time
        data = data_handler.get_data(src_t)

        # Compose HUD (with optional update-rate caching)
        if HUD_CONFIG.get('unified_hud', True):
            hud_rate = HUD_CONFIG.get('hud_update_rate', None)
            do_update = True
            if hud_rate:
                try:
                    interval = 1.0 / float(hud_rate)
                except Exception:
                    interval = None
                if interval is not None and (src_t - hud_cache['t']) < interval and hud_cache['bgr'] is not None:
                    # reuse last HUD
                    hud_bgr = hud_cache['bgr']
                    hud_alpha = hud_cache['alpha']
                    do_update = False

            if do_update:
                hud_bgr, hud_alpha = render_unified_hud(img_bgr, data, data_handler, src_t)
                hud_cache['bgr'] = hud_bgr
                hud_cache['alpha'] = hud_alpha
                hud_cache['t'] = src_t

            if hud_alpha is not None and hud_bgr is not None:
                a3 = np.dstack([hud_alpha, hud_alpha, hud_alpha])
                composed = (img_bgr.astype(np.float32) * (1.0 - a3) + hud_bgr.astype(np.float32) * a3)
                composed = np.clip(composed, 0, 255).astype(np.uint8)
            else:
                composed = img_bgr
        else:
            composed = img_bgr

        # Convert back to RGB for MoviePy
        out_rgb = cv2.cvtColor(composed, cv2.COLOR_BGR2RGB)
        return out_rgb

    # Create a MoviePy VideoClip from our frame function
    video_clip_out = VideoClip(make_frame, duration=duration)

    # Write the file using H.264 (requires ffmpeg). Disable audio to avoid ffmpeg audio issues.
    written_path = None
    # Allow ffmpeg preset selection via config for quality/perf tradeoff
    ff_preset = QUALITY_CONFIG.get('ffmpeg_preset', 'medium') if isinstance(QUALITY_CONFIG, dict) else 'medium'
    ff_threads = int(QUALITY_CONFIG.get('ffmpeg_threads', 4)) if isinstance(QUALITY_CONFIG, dict) else 4

    try:
        video_clip_out.write_videofile(output_file, codec='libx264', fps=fps, audio=False, threads=ff_threads, preset=ff_preset)
        written_path = output_file
    except Exception as e:
        # Common cause: ffmpeg inside container cannot open the target path (permission/SELinux)
        print(f"\n⚠️ Write error: {e}")
        print("   • Trying: write to temp directory and then copy...")

        tmp_dir = tempfile.gettempdir()
        tmp_out = os.path.join(tmp_dir, os.path.basename(output_file))
        try:
            print(f"   • Temp file: {tmp_out}")
            video_clip_out.write_videofile(tmp_out, codec='libx264', fps=fps, audio=False, threads=4, preset='medium')
            # Try to copy back to requested output path (usually /app/... from mounted volume)
            try:
                shutil.copy2(tmp_out, output_file)
                written_path = output_file
                print(f"   • Temp file successfully copied: {output_file}")
            except Exception as copy_err:
                written_path = tmp_out
                print(f"   • Warning: Could not copy to output: {copy_err}")
                print(f"   • Output left in temp location: {tmp_out}")
                print("   • Solution: check file permissions on host or run container with :z, e.g.:")
                print("       podman run --rm -v \"$(pwd):/app:rw,z\" --userns=keep-id video-proje python3 video_renderer.py")
                print("       or run container as root: docker run --rm -u 0 -v \"$(pwd):/app:rw\" video-proje ...")
        except Exception as tmp_err:
            print(f"   • Error: temp write attempt also failed: {tmp_err}")
            raise
    finally:
        # Ensure resources are freed
        try:
            video_clip_out.close()
        except Exception:
            pass
        try:
            clip.close()
        except Exception:
            pass
        clear_gradient_cache()
        # MoviePy prints progress; count estimate based on duration*fps
        frame_count = int(duration * fps)
    
    print(f"\n✅ RENDER COMPLETE!")
    print(f"   • {frame_count} frames processed")
    print(f"   • Duration: {frame_count / fps:.1f}s")
    print(f"   • File: {output_file}")


# ================================================================
#  MAIN
#  ================================================================

if __name__ == "__main__":
    try:
        # Ensure output path is writable before doing heavy work
        out_file = CIKTI_DOSYASI
        base, ext = os.path.splitext(out_file)
        if ext.lower() != '.mp4':
            out_file = base + '.mp4'

        if not ensure_output_writable(out_file):
            print("\n❗ Cannot write to output directory - canceling render.")
            sys.exit(2)

        # Preparation
        clip, data_handler = validate_and_prepare()
        
        # Precompute resources
        W, H = int(clip.size[0]), int(clip.size[1])
        precompute_resources(W, H)
        
        # Render (out_file already validated above)
        render_video(clip, data_handler, out_file)
        
        print("\n" + "="*60)
        print("  ✨ PROCESSING COMPLETE ✨")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process canceled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
