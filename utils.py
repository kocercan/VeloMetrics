# ================================================================
#  YARAYICI FONKSİYONLAR MODÜLÜ (utils.py)
#  ================================================================
#  İçerik:
#  - İçbükey/Konkav arka plan gradient'ları
#  - İkon çizim fonksiyonları (dağ, rota, hız, vb.)
#  - Harita ve navigasyon yardımcıları
#  ================================================================

import cv2
import numpy as np
import math
from config import COLORS, BORDER_RADIUS, QUALITY_CONFIG, OPACITY


# ================================================================
#  İÇBÜKEY ARKA PLAN GRADIENT'LAR
#  ================================================================

# Global gradient cache
_gradient_cache = {}


def create_concave_gradient(w, h):
    """
    İçbükey görünüm için radial gradient oluştur.
    
    Kenarlar koyu, merkez açık olacak şekilde eliptik gradient.
    Doğal 3D cam efekti sağlar.
    
    Args:
        w (int): Genişlik (pixel)
        h (int): Yükseklik (pixel)
    
    Returns:
        np.ndarray: (h, w) şekinde float32 gradient matrisi [0.0-1.0]
    """
    # Return a neutral (near-uniform) gradient matrix so no
    # parabolic/curved/fade-to-center effects are applied.
    # This intentionally avoids any radial or arc math.
    return np.full((h, w), 0.95, dtype=np.float32)


def draw_concave_rect_fast(img, x, y, w, h, radius, base_alpha=0.7):
    """
    Hızlı içbükey yuvarlatılmış dikdörtgen çiz (gradient cache kullanır).
    
    Widget arka planları için optimized fonksiyon.
    Gradient hesaplamalarını cache'ler, böylece her frame'de tekrar hesaplamaz.
    
    Args:
        img (np.ndarray): Hedef resim (BGR)
        x (int): Sol üst X koordinatı
        y (int): Sol üst Y koordinatı
        w (int): Genişlik
        h (int): Yükseklik
        radius (int): Köşe yuvarlatma yarıçapı
        base_alpha (float): Arka plan saydamlığı (0.0-1.0)
    """
    # Draw a flat, rectangular panel with no curved / parabolic effects.
    # Ignore rounded-corner math to keep HUD flat and clean.
    # Clip ROI to image bounds to avoid invalid slices
    ih, iw = img.shape[0], img.shape[1]
    x0 = max(0, int(x))
    y0 = max(0, int(y))
    x1 = min(iw, int(x + w))
    y1 = min(ih, int(y + h))

    if x1 <= x0 or y1 <= y0:
        # Nothing to draw (outside image)
        return

    roi_h = y1 - y0
    roi_w = x1 - x0

    roi = img[y0:y1, x0:x1].copy()

    # Use the configured 'glass' color as base (match roi size)
    color_layer = np.full((roi_h, roi_w, 3), COLORS.get('glass', (30, 30, 30)), dtype=np.uint8)

    # Simple alpha blend using base_alpha (scalar)
    alpha = float(base_alpha)
    blended = (roi * (1 - alpha) + color_layer * alpha).astype(np.uint8)
    img[y0:y1, x0:x1] = blended


def clear_gradient_cache():
    """Gradient cache'i temizle (bellek tasarrufu için)"""
    global _gradient_cache
    _gradient_cache.clear()


# ================================================================
#  İKON ÇİZİM FONKSİYONLARI
#  ================================================================

def draw_mountain_icon(img, cx, cy, size, color):
    """
    Dağ simgesi çiz (yükseklik göstergesi).
    
    Args:
        img: Hedef resim
        cx, cy: Merkez koordinatları
        size: İkon boyutu (pixel)
        color: BGR renk tuple
    """
    s = size
    pts = np.array([
        [cx - s, cy + s//2],
        [cx - s//3, cy - s//2],
        [cx, cy],
        [cx + s//3, cy - s//2 - s//4],
        [cx + s, cy + s//2]
    ], np.int32)
    cv2.polylines(img, [pts], False, color, 2, cv2.LINE_AA)
    # Dağın üstüne kar efekti
    cv2.line(img, (cx + s//3 - 3, cy - s//2 - s//4 + 3), 
             (cx + s//3 + 5, cy - s//2 - s//4 + 6), color, 2, cv2.LINE_AA)


def draw_route_icon(img, cx, cy, size, color):
    """
    Rota simgesi çiz (mesafe göstergesi).
    Dalgalı çizgi + başlangıç noktası.
    """
    s = size
    pts = []
    for i in range(10):
        px = cx - s + (i * s * 2 // 9)
        py = cy + int(math.sin(i * 0.8) * s // 3)
        pts.append([px, py])
    cv2.polylines(img, [np.array(pts, np.int32)], False, color, 2, cv2.LINE_AA)
    # Başlangıç noktası
    cv2.circle(img, (cx - s, cy), 3, color, -1, cv2.LINE_AA)


def draw_speed_icon(img, cx, cy, size, color, val=None):
    """
    Hız göstergesi (speedometer) çiz.
    """
    s = size
    cv2.ellipse(img, (cx, cy + 2), (s, s - 2), 0, 180, 360, color, 2, cv2.LINE_AA)
    # Needle angle mapped from speed (0..70 km/h) -> angles (225..315 degrees)
    # Parse numeric speed if provided via val (string or number)
    sp = None
    try:
        if val is None:
            sp = 0.0
        elif isinstance(val, (int, float)):
            sp = float(val)
        else:
            # try to extract numeric from string
            sp = float(str(val).strip().replace('km/h', '').replace('kmh', '').replace('km', ''))
    except Exception:
        sp = 0.0

    sp = max(0.0, min(70.0, sp))
    min_ang = 225.0
    max_ang = 315.0
    ang_deg = min_ang + (max_ang - min_ang) * (sp / 70.0)
    angle = math.radians(ang_deg)
    # Needle end
    x2 = int(cx + math.cos(angle) * (s - 4))
    y2 = int(cy + 2 + math.sin(angle) * (s - 4))
    cv2.line(img, (cx, cy + 2), (x2, y2), color, 2, cv2.LINE_AA)
    # Center dot
    cv2.circle(img, (cx, cy + 2), 3, color, -1, cv2.LINE_AA)


def draw_gradient_icon(img, cx, cy, size, color, val=None):
    """
    Eğim/Gradient simgesi çiz - görsel olarak yol durumunu gösterir.
    Düz yol, tırmanış, iniş için farklı şekiller.
    """
    s = size
    grade = 0.0
    try:
        if val is not None:
            if isinstance(val, (int, float)):
                grade = float(val)
            else:
                grade = float(str(val).strip().replace('%', ''))
    except Exception:
        grade = 0.0

    if abs(grade) < 1.0:  # Düz yol (-1% ile +1% arası)
        # Düz yol - horizontal çizgi
        cv2.line(img, (cx - s, cy), (cx + s, cy), color, 3, cv2.LINE_AA)
        # Yol kenarları
        cv2.line(img, (cx - s, cy - 2), (cx + s, cy - 2), color, 1, cv2.LINE_AA)
        cv2.line(img, (cx - s, cy + 2), (cx + s, cy + 2), color, 1, cv2.LINE_AA)
        
    elif grade > 1.0:  # Tırmanış
        # Yukarı eğimli yol
        cv2.line(img, (cx - s, cy + s//2), (cx + s, cy - s//2), color, 3, cv2.LINE_AA)
        # Tırmanış oku
        arrow_pts = np.array([
            [cx + s//2, cy - s//2 + 2],
            [cx + s//2 - 4, cy - s//2 + 6],
            [cx + s//2 + 4, cy - s//2 + 6]
        ], np.int32)
        cv2.fillPoly(img, [arrow_pts], color, cv2.LINE_AA)
        # Yol kenarları
        cv2.line(img, (cx - s, cy + s//2 - 2), (cx + s, cy - s//2 - 2), color, 1, cv2.LINE_AA)
        
    else:  # İniş (grade < -1.0)
        # Aşağı eğimli yol
        cv2.line(img, (cx - s, cy - s//2), (cx + s, cy + s//2), color, 3, cv2.LINE_AA)
        # İniş oku
        arrow_pts = np.array([
            [cx + s//2, cy + s//2 - 2],
            [cx + s//2 - 4, cy + s//2 - 6],
            [cx + s//2 + 4, cy + s//2 - 6]
        ], np.int32)
        cv2.fillPoly(img, [arrow_pts], color, cv2.LINE_AA)
        # Yol kenarları
        cv2.line(img, (cx - s, cy - s//2 + 2), (cx + s, cy + s//2 + 2), color, 1, cv2.LINE_AA)


def draw_heart_icon(img, cx, cy, size, color, filled=True):
    """
    Kalp simgesi çiz (kalp atış göstergesi).
    
    Args:
        img: Hedef resim
        cx, cy: Merkez koordinatları
        size: Kalp boyutu
        color: BGR rengi
        filled: True = dolu, False = çerçeve
    """
    s = size
    # Parametrik kalp eğrisi
    pts = []
    for t in np.linspace(0, 2 * math.pi, 50):
        px = 16 * (math.sin(t) ** 3)
        py = -(13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t))
        pts.append([int(cx + px * s / 18), int(cy + py * s / 18 - 2)])
    
    pts = np.array(pts, np.int32)
    if filled:
        cv2.fillPoly(img, [pts], color, cv2.LINE_AA)
    else:
        cv2.polylines(img, [pts], True, color, 2, cv2.LINE_AA)


def draw_cadence_icon(img, cx, cy, size, color):
    """
    Kadans simgesi (dönen çarklar) çiz.
    """
    s = size
    cv2.circle(img, (cx, cy), s, color, 2, cv2.LINE_AA)
    cv2.circle(img, (cx, cy), s//3, color, 2, cv2.LINE_AA)
    # Dış çizgiler
    for i in range(6):
        angle = math.radians(i * 60)
        x1 = int(cx + math.cos(angle) * (s - 2))
        y1 = int(cy + math.sin(angle) * (s - 2))
        x2 = int(cx + math.cos(angle) * (s + 4))
        y2 = int(cy + math.sin(angle) * (s + 4))
        cv2.line(img, (x1, y1), (x2, y2), color, 2, cv2.LINE_AA)


def draw_time_icon(img, cx, cy, size, color):
    """
    Saat simgesi çiz (zaman göstergesi).
    """
    s = size
    cv2.circle(img, (cx, cy), s, color, 2, cv2.LINE_AA)
    # Saat iğneleri
    cv2.line(img, (cx, cy), (cx, cy - s + 3), color, 2, cv2.LINE_AA)
    cv2.line(img, (cx, cy), (cx + s//2, cy + 2), color, 2, cv2.LINE_AA)


def draw_elevation_icon(img, cx, cy, size, color):
    """
    Yükseklik profil simgesi çiz.
    """
    s = size
    pts = np.array([
        [cx - s, cy + s//2],
        [cx - s//2, cy],
        [cx, cy + s//3],
        [cx + s//2, cy - s//2],
        [cx + s, cy - s//3]
    ], np.int32)
    cv2.polylines(img, [pts], False, color, 2, cv2.LINE_AA)


def draw_power_icon(img, cx, cy, size, color, val=None):
    """
    Güç simgesi çiz (lightning bolt).
    
    Args:
        img: Hedef resim
        cx, cy: Merkez koordinatları
        size: İkon boyutu
        color: BGR rengi
        val: Güç değeri (Watt) - animasyon için
    """
    s = size
    
    # Güç değerine göre animasyon
    power = 0
    try:
        if val is not None:
            if isinstance(val, (int, float)):
                power = float(val)
            else:
                power = float(str(val).strip().replace('W', '').replace('w', ''))
    except Exception:
        power = 0
    
    # Güç seviyesine göre boyut ayarlaması (100W = normal, 300W+ = büyük)
    scale = 1.0 + min(0.3, power / 1000)  # Max %30 büyüme
    scaled_s = int(s * scale)
    
    # şimşek şekli
    pts = np.array([
        [cx - scaled_s//3, cy - scaled_s],
        [cx + scaled_s//4, cy - scaled_s//4],
        [cx - scaled_s//4, cy - scaled_s//4],
        [cx + scaled_s//3, cy + scaled_s],
        [cx - scaled_s//4, cy + scaled_s//4],
        [cx + scaled_s//4, cy + scaled_s//4]
    ], np.int32)
    cv2.fillPoly(img, [pts], color, cv2.LINE_AA)
    
    # Yüksek güçte glow efekti
    if power > 200:
        glow_pts = np.array([
            [cx - (scaled_s+2)//3, cy - (scaled_s+2)],
            [cx + (scaled_s+2)//4, cy - (scaled_s+2)//4],
            [cx - (scaled_s+2)//4, cy - (scaled_s+2)//4],
            [cx + (scaled_s+2)//3, cy + (scaled_s+2)],
            [cx - (scaled_s+2)//4, cy + (scaled_s+2)//4],
            [cx + (scaled_s+2)//4, cy + (scaled_s+2)//4]
        ], np.int32)
        glow_color = tuple(int(c * 0.3) for c in color)
        cv2.fillPoly(img, [glow_pts], glow_color, cv2.LINE_AA)


def draw_compass_icon(img, cx, cy, size, color):
    """
    Pusula simgesi çiz (harita göstergesi).
    """
    s = size
    cv2.circle(img, (cx, cy), s, color, 2, cv2.LINE_AA)
    # Kuzey işareti (üçgen)
    pts = np.array([[cx, cy - s + 2], [cx - 3, cy], [cx + 3, cy]], np.int32)
    cv2.fillPoly(img, [pts], color, cv2.LINE_AA)
    # Güney işareti
    cv2.line(img, (cx, cy), (cx, cy + s - 2), color, 1, cv2.LINE_AA)


# ================================================================
#  HARITA VE NAVİGASYON
#  ================================================================

def draw_cyclist_arrow(img, cx, cy, heading, size, color):
    """
    Bisikletçinin konumunu gösteren ok çiz (dönen harita üzerinde).
    
    Okun başı hareket yönüne bakacak şekilde döner.
    
    Args:
        img: Hedef resim
        cx, cy: Merkez koordinatları
        heading: Yön açısı (derece)
        size: Ok boyutu
        color: BGR rengi
    """
    # Ok şekli (yukarı bakan)
    arrow_pts = np.array([
        [0, -size],
        [-size//2, size//2],
        [0, size//4],
        [size//2, size//2]
    ], dtype=np.float32)
    
    # Heading açısına göre döndür
    angle = math.radians(-heading)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    
    rotated = []
    for pt in arrow_pts:
        rx = pt[0] * cos_a - pt[1] * sin_a
        ry = pt[0] * sin_a + pt[1] * cos_a
        rotated.append([int(cx + rx), int(cy + ry)])
    
    rotated = np.array(rotated, np.int32)
    
    # Okun kendisini çiz
    cv2.fillPoly(img, [rotated], color, cv2.LINE_AA)
    cv2.polylines(img, [rotated], True, (255, 255, 255), 1, cv2.LINE_AA)


# ================================================================
#  RENK YARDIMCILARI
#  ================================================================

def get_gradient_color(grade):
    """
    Eğim yüzdesine göre renk belirle.
    
    - < 3%: Yeşil (kolay)
    - 3-8%: Turkuaz (orta)
    - 8-15%: Mor (zor)
    - > 15%: Kırmızı (çok zor)
    
    Args:
        grade (float): Eğim yüzdesi
    
    Returns:
        tuple: BGR renk
    """
    if grade < 3:
        return COLORS['ele_low']
    elif grade < 8:
        ratio = (grade - 3) / 5
        return (
            int(COLORS['ele_low'][0] + ratio * (COLORS['ele_mid'][0] - COLORS['ele_low'][0])),
            int(COLORS['ele_low'][1] + ratio * (COLORS['ele_mid'][1] - COLORS['ele_low'][1])),
            int(COLORS['ele_low'][2] + ratio * (COLORS['ele_mid'][2] - COLORS['ele_low'][2]))
        )
    elif grade < 15:
        ratio = (grade - 8) / 7
        return (
            int(COLORS['ele_mid'][0] + ratio * (COLORS['ele_high'][0] - COLORS['ele_mid'][0])),
            int(COLORS['ele_mid'][1] + ratio * (COLORS['ele_high'][1] - COLORS['ele_mid'][1])),
            int(COLORS['ele_mid'][2] + ratio * (COLORS['ele_high'][2] - COLORS['ele_mid'][2]))
        )
    else:
        return COLORS['ele_high']


if __name__ == "__main__":
    print("✅ Utils module loaded")
