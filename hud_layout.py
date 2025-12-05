import cv2
import numpy as np
import math
from collections import OrderedDict

from config import (
    COLORS, WIDGETS_ENABLED, OPACITY, HUD_CONFIG,
    WIDGET_WIDTH_RATIO, WIDGET_HEIGHT_RATIO, WIDGET_MIN_WIDTH, WIDGET_MIN_HEIGHT,
    BOX_SIZE_RATIO, BOX_SIZE_MIN, PADDING_RATIO, PADDING_MIN, GAP_RATIO, GAP_MIN,
    WIDGET_SCALE, WIDGET_VERTICAL_SHIFT_RATIO,
    PROGRESS_BAR_WIDTH_RATIO, PROGRESS_BAR_HEIGHT
)
from config import TOP_WIDGET_OFFSET_PX
from widgets import (
    draw_panel_v2, draw_heart_panel, draw_pro_map,
    draw_elevation_profile, draw_progress_bar,
    draw_mountain_icon, draw_route_icon, draw_speed_icon,
    draw_gradient_icon, draw_cadence_icon, get_gradient_color
)
from utils import draw_power_icon

# LRU caches to avoid expensive per-frame recomputation
# Use OrderedDict to allow simple LRU eviction when cache grows too large
_distance_cache = OrderedDict()
_remap_cache = OrderedDict()


def _create_distance_map(W, H):
    # Use cache keyed by resolution
    key = (W, H)
    if key in _distance_cache:
        # Move to end (most recently used)
        _distance_cache.move_to_end(key)
        return _distance_cache[key]

    xs = np.arange(W)
    ys = np.arange(H)
    xg, yg = np.meshgrid(xs, ys)
    _distance_cache[key] = (xg, yg)
    # Enforce cache size limit if set in HUD_CONFIG
    try:
        max_entries = int(HUD_CONFIG.get('distance_cache_max_entries', 4))
    except Exception:
        max_entries = 4
    while len(_distance_cache) > max_entries:
        _distance_cache.popitem(last=False)
    return xg, yg


def get_remap_maps(W, H, curve_k):
    """
    Return precomputed remap maps (map_x, map_y) for given resolution
    and curve strength. The map arrays are float32 and ready for
    `cv2.remap`. Cache them to avoid recomputing every frame.
    """
    # Use rounded k to avoid excessive cache entries from tiny floats
    k = float(curve_k)
    k_rounded = round(k, 4)
    key = (W, H, k_rounded)

    if HUD_CONFIG.get('remap_cache_enabled', True) and key in _remap_cache:
        _remap_cache.move_to_end(key)
        return _remap_cache[key]

    xg, yg = _create_distance_map(W, H)
    cx, cy = W // 2, H // 2
    nx = (xg - cx) / (W / 2.0)
    nx2 = nx ** 2
    disp = k * H * nx2

    map_y = np.where(yg < cy, yg + disp, yg - disp).astype(np.float32)
    map_x = xg.astype(np.float32)

    # Clamp maps
    map_x = np.clip(map_x, 0, W - 1).astype(np.float32)
    map_y = np.clip(map_y, 0, H - 1).astype(np.float32)

    if HUD_CONFIG.get('remap_cache_enabled', True):
        _remap_cache[key] = (map_x, map_y)
        try:
            max_entries = int(HUD_CONFIG.get('remap_cache_max_entries', 4))
        except Exception:
            max_entries = 4
        while len(_remap_cache) > max_entries:
            _remap_cache.popitem(last=False)

    return map_x, map_y


def clear_hud_caches():
    """Clear remap and distance caches (call after big resolution change)."""
    _distance_cache.clear()
    _remap_cache.clear()


# (duplicate helper removed)


def render_unified_hud(frame, data, data_handler, t):
    """
    Draw all enabled GPX widgets onto a single HUD layer, apply
    a radial fade toward the screen center and an optional parabolic
    curve. Return (hud_bgr, alpha_mask) where alpha_mask is float32 [0..1].

    - frame: source frame (BGR) used only for size reference
    - data: interpolated GPX/datetime data dict
    - data_handler: DataHandler instance (for points list etc.)
    - t: current time (seconds)

    This function ensures no widget is composited individually onto the
    input frame; instead everything is rendered into one overlay layer.
    """
    H, W = frame.shape[0], frame.shape[1]

    # HUD downscale (render HUD at lower resolution to speed up remap)
    hud_scale = float(HUD_CONFIG.get('hud_downscale', 1.0))
    hud_scale = max(0.25, min(1.0, hud_scale))

    render_W = max(1, int(W * hud_scale))
    render_H = max(1, int(H * hud_scale))

    # Create empty HUD layer at render resolution (BGR)
    hud = np.zeros((render_H, render_W, 3), dtype=frame.dtype)

    # Sizes and layout calculations (same logic as in video_renderer)
    # Apply global widget scale and vertical shift (user-configurable)
    widget_scale = float(WIDGET_SCALE) if 'WIDGET_SCALE' in globals() or 'WIDGET_SCALE' in locals() else float(1.0)
    # Clamp reasonable limits
    widget_scale = max(0.4, min(1.2, widget_scale))

    bw = max(int(render_W * WIDGET_WIDTH_RATIO * widget_scale), int(WIDGET_MIN_WIDTH * widget_scale))
    bh = max(int(render_H * WIDGET_HEIGHT_RATIO * widget_scale), int(WIDGET_MIN_HEIGHT * widget_scale))
    pad = max(int(render_W * PADDING_RATIO * widget_scale), int(PADDING_MIN * widget_scale))
    gap = max(int(render_H * GAP_RATIO * widget_scale), int(GAP_MIN * widget_scale))
    box_size = max(int(min(render_W, render_H) * BOX_SIZE_RATIO * widget_scale), int(BOX_SIZE_MIN * widget_scale))
    bar_w = int(render_W * PROGRESS_BAR_WIDTH_RATIO * widget_scale)
    bar_h = PROGRESS_BAR_HEIGHT

    # Vertical shift (fraction of scaled HUD height). Positive moves widgets down.
    vshift = float(WIDGET_VERTICAL_SHIFT_RATIO)
    vshift_px = int(render_H * vshift)

    # Top widget pixel offset (configurable absolute pixels). Scale to hud resolution.
    try:
        top_offset_px = int(TOP_WIDGET_OFFSET_PX * hud_scale)
    except Exception:
        top_offset_px = 0

    # Heart beat animation phase
    hr = data['hr'] if data['hr'] else 70
    beat_freq = hr / 60.0
    beat_phase = (t * beat_freq * 2 * math.pi) % (2 * math.pi)

    # Draw all widgets onto hud (they draw into provided BGR image)
    # Fast mode control: when enabled, skip expensive features (curve, heavy widgets)
    fast_mode = HUD_CONFIG.get('fast_mode', False)
    curve_enabled = HUD_CONFIG.get('curve_enabled', True) and not fast_mode

    # Left panels (3 widgets)
    pad_y = pad + vshift_px + top_offset_px
    left_widgets = []
    
    if WIDGETS_ENABLED.get('altitude'):
        left_widgets.append(('altitude', data['ele']))
    if WIDGETS_ENABLED.get('distance'):
        left_widgets.append(('distance', data['cum_dist']/1000))
    if WIDGETS_ENABLED.get('gradient'):
        left_widgets.append(('gradient', data['grade']))
    
    for i, (widget_type, value) in enumerate(left_widgets[:3]):
        widget_y = pad_y + (bh + gap) * i
        
        if widget_type == 'altitude':
            draw_panel_v2(hud, pad, widget_y, bw, bh, "ALTITUDE", int(value), "altitude",
                          draw_mountain_icon, COLORS['altitude'])
        elif widget_type == 'distance':
            draw_panel_v2(hud, pad, widget_y, bw, bh, "DISTANCE", value, "distance",
                          draw_route_icon, COLORS['distance'])
        elif widget_type == 'gradient':
            grade_val = value if value is not None else 0.0
            grad_color = get_gradient_color(abs(grade_val))
            draw_panel_v2(hud, pad, widget_y, bw, bh, "GRADIENT", grade_val, "gradient",
                          draw_gradient_icon, grad_color)

    # Right panels (4 widgets)
    right_widgets = []
    
    if WIDGETS_ENABLED.get('speed'):
        right_widgets.append(('speed', data['speed']))
    if WIDGETS_ENABLED.get('heart_rate'):
        right_widgets.append(('heart_rate', data.get('hr')))
    if WIDGETS_ENABLED.get('power'):
        right_widgets.append(('power', data.get('power')))
    if WIDGETS_ENABLED.get('cadence'):
        right_widgets.append(('cadence', data.get('cad')))
    
    # Draw right widgets (max 4)
    for i, (widget_type, value) in enumerate(right_widgets[:4]):
        widget_y = pad_y + (bh + gap) * i
        
        if widget_type == 'speed':
            draw_panel_v2(hud, render_W - pad - bw, widget_y, bw, bh, "SPEED",
                          value, "speed", draw_speed_icon, COLORS['speed'])
        elif widget_type == 'heart_rate' and value is not None:
            draw_heart_panel(hud, render_W - pad - bw, widget_y, bw, bh, value, beat_phase)
        elif widget_type == 'power' and value is not None:
            draw_panel_v2(hud, render_W - pad - bw, widget_y, bw, bh,
                          "POWER", value, "power",
                          draw_power_icon, COLORS['power'])
        elif widget_type == 'cadence' and value is not None:
            draw_panel_v2(hud, render_W - pad - bw, widget_y, bw, bh,
                          "CADENCE", value, "cadence",
                          draw_cadence_icon, COLORS['cadence'])

    # Bottom widgets (skip heavy ones in fast mode)
    if WIDGETS_ENABLED.get('elevation_profile') and not fast_mode:
        # Make elevation widget 50% wider when possible without overlapping the map
        desired_w = int(box_size * 1.5)
        # available space between left pad and map box (approx)
        max_w_allowed = max(box_size, render_W - 3 * pad - box_size - int(20 * widget_scale))
        elev_w = min(desired_w, max_w_allowed)
        draw_elevation_profile(hud, data, pad, render_H - pad - box_size - int(40 * widget_scale) + vshift_px,
                               elev_w, box_size, data_handler.points)

    if WIDGETS_ENABLED.get('route_map') and not fast_mode:
        draw_pro_map(hud, data, render_W - pad - box_size, render_H - pad - box_size - int(40 * widget_scale) + vshift_px,
                    box_size, data_handler.points)

    if WIDGETS_ENABLED.get('progress_bar'):
        bx = (render_W - bar_w) // 2
        by = render_H - int(35 * hud_scale) + vshift_px
        elapsed_seconds = int(t)
        from datetime import timedelta
        time_str = str(timedelta(seconds=elapsed_seconds))[2:7]
        draw_progress_bar(hud, bx, by, bar_w, bar_h, data['progress'], time_str)

    # Compute diff mask where HUD painted (scaled)
    diff_mask = np.any(hud != 0, axis=2)
    if not np.any(diff_mask):
        # Nothing drawn
        return np.zeros((H, W, 3), dtype=np.uint8), np.zeros((H, W), dtype=np.float32)

    # Prepare alpha mask: classify background vs content (text/icons)
    # Use luminance to estimate background (dark glass areas)
    bgr = hud.astype(np.float32)
    lum = 0.2126 * bgr[:, :, 2] + 0.7152 * bgr[:, :, 1] + 0.0722 * bgr[:, :, 0]
    bg_thresh = HUD_CONFIG.get('bg_lum_threshold', 90)
    background_mask = (lum < bg_thresh) & diff_mask
    content_mask = diff_mask & (~background_mask)

    # Radial fade toward screen center (use scaled coords)
    cx, cy = render_W // 2, render_H // 2
    xg, yg = _create_distance_map(render_W, render_H)
    dist = np.sqrt((xg - cx) ** 2 + (yg - cy) ** 2)
    maxd = np.sqrt(cx ** 2 + cy ** 2)
    nd = np.clip(dist / (maxd + 1e-6), 0.0, 1.0)
    fade_strength = HUD_CONFIG.get('fade_strength', 0.9)
    # alpha factor for backgrounds: edges keep base alpha, center becomes more transparent
    alpha_bg_factor = 1.0 - fade_strength * (1.0 - nd)

    # Base background alpha: use the larger of small/large panel alphas
    base_bg_alpha = max(OPACITY.get('panel_bg_alpha', 0.7), OPACITY.get('panel_bg_alpha_large', 0.75))

    alpha_map = np.zeros((render_H, render_W), dtype=np.float32)
    alpha_map[background_mask] = base_bg_alpha * alpha_bg_factor[background_mask]
    alpha_map[content_mask] = 1.0

    # Ensure values in [0,1]
    alpha_map = np.clip(alpha_map, 0.0, 1.0)

    # Build RGBA HUD for remapping
    alpha_chan = (alpha_map * 255).astype(np.uint8)
    hud_rgba = np.dstack((hud, alpha_chan))

    # Apply parabolic curve if enabled (use cached remap maps)
    # Prepare for remap / curve
    if curve_enabled and HUD_CONFIG.get('curve_strength', 0.0) > 0.0:
        k = float(HUD_CONFIG.get('curve_strength', 0.18))
        try:
            # Get remap maps at scaled resolution
            map_x_full, map_y_full = get_remap_maps(render_W, render_H, k)

            if HUD_CONFIG.get('roi_remap', True):
                # Crop to HUD ROI to reduce remap work
                ys, xs = np.where(np.any(hud_rgba[:, :, :4] != 0, axis=2))
                if len(xs) == 0 or len(ys) == 0:
                    warped = hud_rgba
                else:
                    x0, x1 = int(xs.min()), int(xs.max()) + 1
                    y0, y1 = int(ys.min()), int(ys.max()) + 1

                    # Expand ROI vertically to account for parabolic remap displacement
                    # so that content shifted upward by the curve isn't clipped.
                    # Estimate maximum vertical displacement (in pixels) as k * render_H
                    try:
                        k = float(HUD_CONFIG.get('curve_strength', 0.0))
                    except Exception:
                        k = 0.0
                    margin = int(abs(k) * render_H) + 4
                    y0 = max(0, y0 - margin)
                    y1 = min(render_H, y1 + margin)

                    map_x_roi = map_x_full[y0:y1, x0:x1]
                    map_y_roi = map_y_full[y0:y1, x0:x1]

                    src = hud_rgba
                    # Remap only ROI
                    warped_roi = cv2.remap(src, map_x_roi, map_y_roi,
                                           interpolation=cv2.INTER_LINEAR,
                                           borderMode=cv2.BORDER_CONSTANT,
                                           borderValue=(0, 0, 0, 0))

                    # Place into full warped canvas
                    warped = np.zeros_like(hud_rgba)
                    warped[y0:y1, x0:x1] = warped_roi
            else:
                warped = cv2.remap(hud_rgba, map_x_full, map_y_full,
                                   interpolation=cv2.INTER_LINEAR,
                                   borderMode=cv2.BORDER_CONSTANT,
                                   borderValue=(0, 0, 0, 0))
        except Exception:
            # Fallback: no warp
            warped = hud_rgba
    else:
        warped = hud_rgba

    # Split back (still scaled)
    warped_bgr_small = warped[:, :, :3]
    warped_alpha_small = warped[:, :, 3].astype(np.float32) / 255.0

    # Upscale to original frame resolution if we rendered at lower res
    if hud_scale < 1.0:
        warped_bgr = cv2.resize(warped_bgr_small, (W, H), interpolation=cv2.INTER_LINEAR)
        warped_alpha = cv2.resize(warped_alpha_small, (W, H), interpolation=cv2.INTER_LINEAR)
    else:
        warped_bgr = warped_bgr_small
        warped_alpha = warped_alpha_small

    return warped_bgr, warped_alpha
