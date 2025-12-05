# ================================================================
#  WIDGET VE PANEL MODÜlÜ (widgets.py)
#  ================================================================
#  İçerik:
#  - Panel ve widget çizimi
#  - Kalp atış paneli (Zone göstergesi ile)
#  - Yükseklik profili grafik
#  - Dönen harita
#  - İlerleme çubuğu
#  ================================================================

import cv2
import numpy as np
import math

from config import (
    COLORS, BORDER_RADIUS, OPACITY, FONT_CONFIG, 
    WIDGETS_ENABLED, ADVANCED_CONFIG, UNIT_SYSTEM, UNIT_CONVERSIONS, UNIT_LABELS
)
from utils import (
    draw_concave_rect_fast, draw_mountain_icon, draw_route_icon,
    draw_speed_icon, draw_gradient_icon, draw_heart_icon,
    draw_cadence_icon, draw_time_icon, draw_elevation_icon,
    draw_compass_icon, draw_cyclist_arrow, get_gradient_color
)
from data_handler import get_hr_zone

def format_value(value, unit_type):
    """Format value according to unit system"""
    if value is None:
        return "--", UNIT_LABELS[UNIT_SYSTEM][unit_type]
    
    factor = UNIT_CONVERSIONS[UNIT_SYSTEM][unit_type]
    unit = UNIT_LABELS[UNIT_SYSTEM][unit_type]
    converted_value = value * factor
    
    # Format based on unit type
    if unit_type == 'distance':
        return f"{converted_value:.1f}", unit
    elif unit_type == 'altitude':
        return f"{int(converted_value)}", unit
    elif unit_type == 'speed':
        return f"{converted_value:.1f}", unit
    elif unit_type == 'gradient':
        return f"{converted_value:.1f}", unit
    else:
        return f"{converted_value:.1f}", unit


# ---------------------
# Text rendering helper
# ---------------------
try:
    has_freetype = hasattr(cv2, 'freetype') and hasattr(cv2.freetype, 'createFreeType2')
except Exception:
    has_freetype = False

def _resolve_face(name):
    # name may be a cv2 constant name string like 'FONT_HERSHEY_SIMPLEX'
    if isinstance(name, int):
        return name
    if not name:
        return cv2.FONT_HERSHEY_SIMPLEX
    try:
        return getattr(cv2, name)
    except Exception:
        return cv2.FONT_HERSHEY_SIMPLEX

def draw_text(img, text, org, face_name, font_scale, color, thickness_float, line_type=None, outline=None, outline_color=None):
    """
    Unified text drawing helper.

    - Accepts float `thickness_float` for finer control; it is rounded
      when calling OpenCV which requires integer thickness.
    - Draws an outline/stroke behind the main text for readability on
      varying backgrounds (white/black/grey).
    - If FreeType is configured and available, widgets may opt-in to
      use TTF rendering (not automatic here).
    """
    if line_type is None:
        line_type = cv2.LINE_AA

    face = _resolve_face(face_name)

    # Convert to integer thickness for cv2 calls, but allow 0 (thin)
    eff_th = max(0, int(round(thickness_float)))

    # Outline defaults
    if outline is None:
        outline = FONT_CONFIG.get('outline_enabled', True)
    if outline_color is None:
        oc = FONT_CONFIG.get('outline_color', (0, 0, 0))
        outline_color = oc

    if outline and eff_th >= 0:
        # Outline thickness as multiplier of user thickness (float)
        out_mul = float(FONT_CONFIG.get('outline_strength', 1.4))
        out_th = max(1, int(round(thickness_float * out_mul)))
        # Draw a stamped outline by offsetting the text a few pixels in a
        # small grid. This produces a visible halo/stroke even for small
        # font sizes and makes fractional thickness perceptible.
        # Limit radius for performance.
        radius = min(3, out_th)
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                pos = (org[0] + dx, org[1] + dy)
                cv2.putText(img, text, pos, face, font_scale, outline_color, max(1, int(round(out_th/2))), line_type)

    # Main text
    cv2.putText(img, text, org, face, font_scale, color, eff_th, line_type)


# ================================================================
#  TEMEL PANEL
#  ================================================================

def draw_panel_v2(img, x, y, w, h, title, value, unit_type, icon_func, icon_color):
    """
    Standart veri paneli çiz (yükseklik, mesafe, hız vb.).
    
    Layout:
    ┌─────────────────────┐
    │ [icon] TITLE        │
    │ [icon] VALUE unit   │
    └─────────────────────┘
    
    Args:
        img: Hedef resim (BGR)
        x, y: Sol üst köşe koordinatı
        w, h: Panel genişliği/yüksekliği
        title: Başlık (örn: "ALTITUDE")
        value: Gösterilecek değer
        unit_type: Birim tipi (örn: "altitude", "speed")
        icon_func: İkon çizme fonksiyonu
        icon_color: İkon rengi
    """
    # İçbükey arka plan
    draw_concave_rect_fast(img, x, y, w, h, BORDER_RADIUS['panel_corner'], 
                          OPACITY['panel_bg_alpha'])

    # Icon sizing and margins now relative to panel height (avoid fixed offsets)
    icon_margin = max(6, int(h * 0.12))
    icon_box_size = max(12, h - 2 * icon_margin)
    icon_x = x + icon_margin
    icon_y = y + icon_margin

    # Draw icon centered inside icon box
    # Try passing the panel value as an extra argument to icon functions that accept it
    try:
        icon_func(img, icon_x + icon_box_size // 2, icon_y + icon_box_size // 2,
                  int(icon_box_size * ADVANCED_CONFIG['icon_size_ratio']), icon_color, value)
    except TypeError:
        # Fallback for icon functions that don't accept a value parameter
        icon_func(img, icon_x + icon_box_size // 2, icon_y + icon_box_size // 2,
                  int(icon_box_size * ADVANCED_CONFIG['icon_size_ratio']), icon_color)

    # Text positions computed from panel height for better scaling
    text_x = icon_x + icon_box_size + max(8, int(h * 0.08))
    title_size_local = FONT_CONFIG['title_size']
    title_thickness_local = FONT_CONFIG['title_thickness']
    title_color_local = COLORS['text_main']
    unit_size_local = FONT_CONFIG['unit_size']
    unit_thickness_local = FONT_CONFIG['unit_thickness']

    title_y = y + max(16, int(h * 0.28))
    value_y = y + h - max(8, int(h * 0.16))

    # Başlık metni
    draw_text(img, title, (text_x, title_y), FONT_CONFIG.get('font_face_title'), title_size_local, title_color_local, title_thickness_local, line_type=cv2.LINE_AA)

    # Format value according to unit system
    val_str, unit = format_value(value, unit_type)
    draw_text(img, val_str, (text_x, value_y), FONT_CONFIG.get('font_face_value'), FONT_CONFIG['value_size'], COLORS['text_main'], FONT_CONFIG['value_thickness'], line_type=cv2.LINE_AA)

    # Birim metni (place to the right of value)
    (vw, vh), _ = cv2.getTextSize(val_str, _resolve_face(FONT_CONFIG.get('font_face_value')), 
                                  FONT_CONFIG['value_size'], 
                                  max(1, int(round(FONT_CONFIG['value_thickness']))))
    draw_text(img, unit, (text_x + vw + max(4, int(h * 0.03)), value_y), FONT_CONFIG.get('font_face_unit'), unit_size_local, title_color_local if title_color_local == COLORS['text_main'] else COLORS['text_sub'], unit_thickness_local, line_type=cv2.LINE_AA)


# ================================================================
#  KALP ATIŞI PANELİ - ZONE SİSTEMİ İLE
#  ================================================================

def draw_heart_panel(img, x, y, w, h, hr_value, beat_phase=0):
    """
    Kalp atış paneli - Zone göstergesi ve animasyon ile.
    
    Layout:
    ┌──────────────────────────────────────┐
    │ [ZONE]  HEART RATE               BPM │
    │ [animating heart] 120 bpm            │
    │ ◼ ◼ ◼ ◼ ◼  (Zone bar - 5 segment)   │
    └──────────────────────────────────────┘
    
    Args:
        img: Hedef resim
        x, y: Konum
        w, h: Boyut
        hr_value: Kalp atış hızı (bpm)
        beat_phase: Animasyon fazı (0-2π)
    """
    # İçbükey arka plan
    draw_concave_rect_fast(img, x, y, w, h, BORDER_RADIUS['panel_corner'], 
                          OPACITY['panel_bg_alpha'])

    # Zone bilgisini al
    zone_num, zone_color, zone_text = get_hr_zone(hr_value)

    # Icon sizes relative to panel height
    icon_margin = max(6, int(h * 0.12))
    icon_size = max(12, h - 2 * icon_margin)
    icon_cx = x + icon_margin + icon_size // 2
    icon_cy = y + h // 2

    # Kalp atış animasyonu - size mapped to configured heartbeat scale
    heart_scale_min = ADVANCED_CONFIG['heart_beat_scale_min']
    heart_scale_max = ADVANCED_CONFIG['heart_beat_scale_max']
    heart_scale = heart_scale_min + int((heart_scale_max - heart_scale_min) * (1 + math.sin(beat_phase)) / 2)

    draw_heart_icon(img, icon_cx, icon_cy, heart_scale, zone_color, filled=True)

    # Başlık and value positions (relative) - adjusted for better spacing
    text_x = x + icon_margin + icon_size + max(8, int(h * 0.08))
    title_y = y + max(14, int(h * 0.25))
    value_y = y + h - max(20, int(h * 0.35))  # Move up to make room for zone bar

    draw_text(img, "HEART RATE", (text_x, title_y), FONT_CONFIG.get('font_face_title'), FONT_CONFIG['title_size'], COLORS['text_main'], FONT_CONFIG['title_thickness'], line_type=cv2.LINE_AA)

    hr_str = str(int(hr_value)) if hr_value else "--"
    draw_text(img, hr_str, (text_x, value_y), FONT_CONFIG.get('font_face_value'), FONT_CONFIG['value_size'], COLORS['text_main'], FONT_CONFIG['value_thickness'], line_type=cv2.LINE_AA)

    (vw, _), _ = cv2.getTextSize(hr_str, _resolve_face(FONT_CONFIG.get('font_face_value')), 
                                 FONT_CONFIG['value_size'], 
                                 max(1, int(round(FONT_CONFIG['value_thickness']))))
    draw_text(img, "bpm", (text_x + vw + max(4, int(h * 0.03)), value_y), FONT_CONFIG.get('font_face_unit'), FONT_CONFIG['unit_size'], COLORS['text_sub'], FONT_CONFIG['unit_thickness'], line_type=cv2.LINE_AA)

    # Zone indicator (top right corner) - pill shaped (büyütülmüş)
    if zone_num and WIDGETS_ENABLED.get('heart_rate', True):
        zone_w = 58  # 50'den 58'e büyütüldü
        zone_h = 16  # 14'ten 16'ya büyütüldü
        zone_x = x + w - zone_w - 6
        zone_y = y + 6
        
        # Zone pill background (rounded)
        radius = zone_h // 2
        cv2.circle(img, (zone_x + radius, zone_y + radius), radius, zone_color, -1, cv2.LINE_AA)
        cv2.rectangle(img, (zone_x + radius, zone_y), (zone_x + zone_w - radius, zone_y + zone_h), zone_color, -1)
        cv2.circle(img, (zone_x + zone_w - radius, zone_y + radius), radius, zone_color, -1, cv2.LINE_AA)
        
        # Zone text with siliklestirilen outline (outline_color alpha azaltıldı)
        draw_text(img, zone_text, (zone_x + 5, zone_y + 12), FONT_CONFIG.get('font_face_small'), FONT_CONFIG['small_size'], (255, 255, 255), FONT_CONFIG['small_thickness'], line_type=cv2.LINE_AA, outline_color=(0, 0, 0), outline=True)

    # Zone bar (5 segments) - positioned at bottom
    if WIDGETS_ENABLED.get('heart_rate', True):
        bar_y = y + h - max(8, int(h * 0.15))
        bar_width = w - 2 * icon_margin
        bar_height = max(3, int(h * 0.06))
        segment_width = bar_width // 5
        
        for i in range(1, 6):
            seg_x = x + icon_margin + (i-1) * segment_width
            seg_color = COLORS[f'zone{i}'] if i == zone_num else (60, 60, 60)
            cv2.rectangle(img, (seg_x, bar_y), (seg_x + segment_width - 2, bar_y + bar_height), seg_color, -1)


# ================================================================
#  HARITA VE ELEVASİON PROFİLİ
#  ================================================================

def draw_pro_map(img, data, x, y, size, points_list):
    """
    Dönen harita çiz (bisikletçi merkez, rota ön/geri).
    
    Harita merkezi bisikletçinin konumunda,
    hareket yönüne göre döner (heading).
    
    Args:
        img: Hedef resim
        data: get_data() çıkışı (lat, lon, heading, idx)
        x, y: Harita sol üst köşesi
        size: Harita kutusu boyutu
        points_list: Tüm waypoint'ler
    """
    if not WIDGETS_ENABLED.get('route_map'):
        return
    
    # İçbükey arka plan
    draw_concave_rect_fast(img, x, y, size, size, BORDER_RADIUS['large_box_corner'], 
                          OPACITY['panel_bg_alpha_large'])
    
    # Başlık
    draw_compass_icon(img, x + 18, y + 16, 7, COLORS['accent'])
    draw_text(img, "ROUTE MAP", (x + 32, y + 20), FONT_CONFIG.get('font_face_title'), FONT_CONFIG['title_size'], COLORS['text_main'], FONT_CONFIG['title_thickness'], line_type=cv2.LINE_AA)
    
    # Harita merkezi
    map_cx = x + size // 2
    map_cy = y + size // 2 + 10
    map_radius = size // 2 - 20
    
    # Hareket yönüne göre dönüş
    heading_rad = math.radians(-data['heading'])
    cos_h, sin_h = math.cos(heading_rad), math.sin(heading_rad)
    
    # Gösterilecek point range'i
    from config import MAP_CONFIG
    range_pts = MAP_CONFIG['display_range']
    start_i = max(0, data['idx'] - range_pts)
    end_i = min(len(points_list), data['idx'] + range_pts)
    
    past_pts = []
    future_pts = []
    
    # Noktaları harita koordinatına dönüştür
    for i in range(start_i, end_i):
        p = points_list[i]
        
        # Bisikletçiye göre relatif konum (derece)
        dx = (p['lon'] - data['lon']) * MAP_CONFIG['zoom_factor']
        dy = (data['lat'] - p['lat']) * MAP_CONFIG['zoom_factor'] * 1.4
        
        # Heading'e göre döndür
        rx = dx * cos_h - dy * sin_h
        ry = dx * sin_h + dy * cos_h
        
        px = int(map_cx + rx)
        py = int(map_cy + ry)
        
        # Harita sınırları içinde mi?
        dist_from_center = math.sqrt((px - map_cx)**2 + (py - map_cy)**2)
        if dist_from_center < map_radius:
            if i < data['idx']:
                past_pts.append((px, py))
            else:
                future_pts.append((px, py))
    
    # Geçmiş rota (gri, ince)
    if len(past_pts) > 1:
        cv2.polylines(img, [np.array(past_pts)], False, COLORS['map_path'], 
                     3, cv2.LINE_AA)
    
    # Gelecek rota (açık + vurgu)
    if len(future_pts) > 1:
        cv2.polylines(img, [np.array(future_pts)], False, COLORS['map_path_front'], 
                     4, cv2.LINE_AA)
        cv2.polylines(img, [np.array(future_pts)], False, COLORS['accent'], 
                     2, cv2.LINE_AA)
    
    # Bisikletçi okunu çiz (merkez)
    draw_cyclist_arrow(img, map_cx, map_cy, 0, 14, COLORS['accent'])
    
    # Mini pusula (sağ alt)
    compass_x = x + size - 25
    compass_y = y + size - 25
    cv2.circle(img, (compass_x, compass_y), 12, (40, 40, 40), -1, cv2.LINE_AA)
    cv2.circle(img, (compass_x, compass_y), 12, (70, 70, 70), 1, cv2.LINE_AA)
    
    # Kuzey işareti (N)
    n_angle = heading_rad
    nx = int(compass_x + math.sin(n_angle) * 8)
    ny = int(compass_y - math.cos(n_angle) * 8)
    cv2.line(img, (compass_x, compass_y), (nx, ny), (100, 100, 255), 2, cv2.LINE_AA)
    draw_text(img, "N", (nx - 4, ny - 3), FONT_CONFIG.get('font_face_small'), FONT_CONFIG['small_size'], (100, 100, 255), FONT_CONFIG['small_thickness'], line_type=cv2.LINE_AA)


# ================================================================
#  EĞİM PROFİLİ GRAFİĞİ
#  ================================================================

def draw_elevation_profile(img, data, x, y, w, h, points_list):
    """
    Yükseklik profili grafik çiz.
    
    Grafiğin ortasında mevcut konum belirtilir.
    Eğim yüzdesine göre renk değişir.
    
    Args:
        img: Hedef resim
        data: get_data() çıkışı
        x, y: Sol üst köşe
        w, h: Boyut
        points_list: Tüm waypoint'ler
    """
    if not WIDGETS_ENABLED.get('elevation_profile'):
        return
    
    # İçbükey arka plan
    draw_concave_rect_fast(img, x, y, w, h, BORDER_RADIUS['large_box_corner'], 
                          OPACITY['panel_bg_alpha_large'])
    
    # Başlık
    draw_elevation_icon(img, x + 18, y + 16, 7, COLORS['altitude'])
    draw_text(img, "ELEVATION", (x + 32, y + 20), FONT_CONFIG.get('font_face_title'), FONT_CONFIG['title_size'], COLORS['text_main'], FONT_CONFIG['title_thickness'], line_type=cv2.LINE_AA)
    
    # Grafik alanı
    graph_x = x + 15
    graph_y = y + 35
    graph_w = w - 30
    graph_h = h - 60
    
    from config import ELEVATION_PROFILE
    display_range = ELEVATION_PROFILE['display_range']
    
    # Mevcut konumun etrafında range
    center_idx = data['idx']
    start_i = max(0, center_idx - display_range // 2)
    end_i = min(len(points_list), center_idx + display_range // 2)
    
    if end_i - start_i < ELEVATION_PROFILE['min_points']:
        return  # Çok az point
    
    # Min/max yükseklik bulunsan
    ele_values = [points_list[i]['ele'] for i in range(start_i, end_i)]
    min_ele = min(ele_values) - 5
    max_ele = max(ele_values) + 5
    ele_range = max_ele - min_ele if max_ele > min_ele else 1
    
    # Grafik noktalarını hesapla
    graph_pts = []
    colors_at_pts = []
    
    for i, idx in enumerate(range(start_i, end_i)):
        # X koordinatı (yatay)
        px = graph_x + int((i / (end_i - start_i - 1)) * graph_w)
        
        # Y koordinatı (yükseklik normalize)
        ele_norm = (points_list[idx]['ele'] - min_ele) / ele_range
        from config import ADVANCED_CONFIG
        vscale = float(ADVANCED_CONFIG.get('elevation_vertical_scale', 1.0))
        # Compress vertical amplitude around center to reduce steepness
        scaled_norm = 0.5 + (ele_norm - 0.5) * vscale
        py = graph_y + graph_h - int(scaled_norm * graph_h)
        
        graph_pts.append((px, py))
        
        # Eğim hesapla (renk için) - use precomputed seg_dist when available
        if idx > 0:
            d = points_list[idx].get('seg_dist', None)
            if d is None:
                # Fast equirectangular approx fallback (meters)
                lat1 = math.radians(points_list[idx-1]['lat'])
                lat2 = math.radians(points_list[idx]['lat'])
                dlat = lat2 - lat1
                dlon = math.radians(points_list[idx]['lon'] - points_list[idx-1]['lon'])
                # mean latitude scale
                mean_lat = (lat1 + lat2) / 2.0
                m_per_deg_lat = 111132.92 - 559.82 * math.cos(2 * mean_lat) + 1.175 * math.cos(4 * mean_lat)
                m_per_deg_lon = 111412.84 * math.cos(mean_lat) - 93.5 * math.cos(3 * mean_lat)
                approx = math.sqrt((dlat * m_per_deg_lat) ** 2 + (dlon * m_per_deg_lon) ** 2)
                d = approx

            if d > 1:
                grade = abs(points_list[idx]['ele'] - points_list[idx-1]['ele']) / d * 100
            else:
                grade = 0
        else:
            grade = 0
        
        colors_at_pts.append(get_gradient_color(grade))
    
    # Grafiği çiz
    if len(graph_pts) > 2:
        # Area fill (flat) - draw filled polygon without extra blending
        fill_pts = list(graph_pts)
        fill_pts.append((graph_pts[-1][0], graph_y + graph_h))
        fill_pts.append((graph_pts[0][0], graph_y + graph_h))
        cv2.fillPoly(img, [np.array(fill_pts)], (40, 40, 40), cv2.LINE_AA)

        # Line
        for i in range(len(graph_pts) - 1):
            cv2.line(img, graph_pts[i], graph_pts[i+1], colors_at_pts[i], 2, cv2.LINE_AA)
    
    # Mevcut konum göstergesi
    current_rel_idx = center_idx - start_i
    if 0 <= current_rel_idx < len(graph_pts):
        curr_pt = graph_pts[current_rel_idx]
        
        # Dikey çizgi
        cv2.line(img, (curr_pt[0], graph_y), (curr_pt[0], graph_y + graph_h), 
                (70, 70, 70), 1, cv2.LINE_AA)
        
        # Vurgulu nokta
        cv2.circle(img, curr_pt, 6, COLORS['accent'], -1, cv2.LINE_AA)
        cv2.circle(img, curr_pt, 6, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Yükseklik bilgisi (with unit conversion)
        ele_val, ele_unit = format_value(data['ele'], 'altitude')
        draw_text(img, f"{ele_val}{ele_unit}", (curr_pt[0] - 15, curr_pt[1] - 10), FONT_CONFIG.get('font_face_small'), FONT_CONFIG['small_size'], COLORS['text_main'], FONT_CONFIG['small_thickness'], line_type=cv2.LINE_AA)
    
    # Min/Max yükseklik labels (with unit conversion)
    max_val, unit = format_value(max_ele, 'altitude')
    min_val, _ = format_value(min_ele, 'altitude')
    draw_text(img, f"{max_val}{unit}", (x + w - 40, graph_y + 12), FONT_CONFIG.get('font_face_small'), FONT_CONFIG['small_size'], COLORS['text_sub'], FONT_CONFIG['small_thickness'], line_type=cv2.LINE_AA)
    draw_text(img, f"{min_val}{unit}", (x + w - 40, graph_y + graph_h - 2), FONT_CONFIG.get('font_face_small'), FONT_CONFIG['small_size'], COLORS['text_sub'], FONT_CONFIG['small_thickness'], line_type=cv2.LINE_AA)
    
    # İlerleme yüzdesi
    progress_str = f"{data['progress']:.1f}%"
    draw_text(img, progress_str, (x + w//2 - 20, y + h - 8), FONT_CONFIG.get('font_face_title'), FONT_CONFIG['title_size'], COLORS['accent'], FONT_CONFIG['title_thickness'], line_type=cv2.LINE_AA)


# ================================================================
#  İLERLEME ÇUBUĞU
#  ================================================================

def draw_progress_bar(img, x, y, w, h, progress, time_str):
    """
    İlerleme çubuğu çiz (bottom center).
    
    Args:
        img: Hedef resim
        x, y: Çubuğun sol üst köşesi
        w, h: Boyut
        progress: İlerleme % (0-100)
        time_str: Zaman string (HH:MM:SS formatı)
    """
    if not WIDGETS_ENABLED.get('progress_bar'):
        return
    
    # İçbükey arka plan
    draw_concave_rect_fast(img, x, y - 5, w, h + 10, BORDER_RADIUS['panel_corner'], 
                          OPACITY['panel_bg_alpha'] * 0.5)
    
    # Dolgu (filled)
    fill_w = int((w - 4) * (progress / 100))
    if fill_w > ADVANCED_CONFIG['progress_bar_min_width']:
        # Draw the filled progress area (flat)
        cv2.rectangle(img, (x + 2, y + 2), (x + 2 + fill_w, y + h - 2), COLORS['accent'], -1)
    
    # Zaman display
    draw_time_icon(img, x + w//2 - 45, y - 18, 7, COLORS['text_sub'])
    draw_text(img, time_str, (x + w//2 - 30, y - 13), FONT_CONFIG.get('font_face_title'), FONT_CONFIG['title_size'] + 0.1, COLORS['text_main'], FONT_CONFIG['title_thickness'], line_type=cv2.LINE_AA)
    
    # Yüzde göstergesi
    pct_str = f"{progress:.1f}%"
    draw_text(img, pct_str, (x + w + 8, y + h - 1), FONT_CONFIG.get('font_face_title'), FONT_CONFIG['title_size'], COLORS['text_sub'], FONT_CONFIG['title_thickness'], line_type=cv2.LINE_AA)


if __name__ == "__main__":
    print("✅ Widgets module loaded")
    print("   • draw_panel_v2()")
    print("   • draw_heart_panel()")
    print("   • draw_pro_map()")
    print("   • draw_elevation_profile()")
    print("   • draw_progress_bar()")