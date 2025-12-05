# ================================================================
#  GELİŞMİŞ AYARLAR - ADVANCED SETTINGS
# ================================================================
#  Bu dosya gelişmiş kullanıcılar için detaylı ayarları içerir
#  This file contains detailed settings for advanced users
# ================================================================

import os

# ==================== NOT: TEMEL AYARLAR config.py'YE TAŞINDI ====================
# ==================== NOTE: BASIC SETTINGS MOVED TO config.py ====================
"""
POWER_CONFIG, HR_ZONES, MAP_CONFIG ve USER_AGE artık config.py'de
POWER_CONFIG, HR_ZONES, MAP_CONFIG and USER_AGE are now in config.py
"""

# ==================== KÖŞE YUVARLATMA ====================
# ==================== CORNER ROUNDING ====================
"""
Widget'lar ve box'lar için köşe yuvarlatma yarıçapı
Corner rounding radius for widgets and boxes
"""
BORDER_RADIUS = {
    'panel_corner': 10,         # Küçük paneller için / For small panels
    'large_box_corner': 12,     # Harita/Eğim kutuları için / For map/elevation boxes
}

# ==================== PERFORMANS VE KALİTE AYARLARI ====================
# ==================== PERFORMANCE AND QUALITY SETTINGS ====================
"""
Render kalitesi ve hızı arasında denge
Balance between render quality and speed
"""
QUALITY_CONFIG = {
    # Antialiasing
    'use_antialiasing': True,   # True = daha güzel ama daha yavaş / True = prettier but slower
    'line_aa': 'cv2.LINE_AA',   # Anti-aliased çizgiler / Anti-aliased lines
    
    # Gradient cache
    'cache_gradients': True,    # Gradient'ları hafızada tut (hızlı ama RAM kullanır) / Keep gradients in memory (fast but uses RAM)
    
    # Konvolüsyon işlemleri / Convolution operations
    'use_vectorization': True,  # NumPy vektörization (hızlı çizim) / NumPy vectorization (fast drawing)
    
    # Pre-compute
    'precompute_gradients': True,  # Başında gradient'ları hesapla / Calculate gradients at start
    'precompute_convex_map': False,  # Konveks harita (şimdi KALDIRILDı) / Convex map (now REMOVED)
}

# ==================== HARITA İZLEME ====================
# ==================== MAP TRACKING ====================
"""
Harita çizimindeki puan/waypoint yoğunluğu
Point/waypoint density in map drawing
"""
ELEVATION_PROFILE = {
    'display_range': 200,       # Kaç waypoint gösterilir / How many waypoints to show
    'min_points': 10,           # Minimum puan sayısı grafik için / Minimum point count for chart
}

# ==================== ÖZEL AYARLAR ====================
# ==================== SPECIAL SETTINGS ====================
"""
Ekstra tweaking için gelişmiş ayarlar
Advanced settings for extra tweaking
"""
ADVANCED_CONFIG = {
    # İkon boyutları / Icon sizes
    'icon_size_ratio': 1/3,     # İkon paneli içerisinde oran / Icon ratio within panel
    
    # Kalp atış animasyon / Heart rate animation
    'heart_beat_scale_min': 9,  # Kalp minimum boyutu / Heart minimum size
    'heart_beat_scale_max': 11, # Kalp maksimum boyutu / Heart maximum size
    'heart_beat_glow_min': 0.5, # Glow minimum scale
    'heart_beat_glow_max': 0.58,  # Glow maximum scale
    
    # Eğim renk sınırları / Gradient color thresholds
    'elevation_color_thresholds': {
        'low': 3,               # < 3% = yeşil / < 3% = green
        'mid': 8,               # 3-8% = turkuaz / 3-8% = turquoise
        'high': 15,             # 8-15% = kırmızı-mor / 8-15% = red-purple
        # > 15% = çok kırmızı / > 15% = very red
    },
    
    # Harita shadow/glow / Map shadow/glow
    'map_shadow_offset': 2,     # Pixel cinsinden shadow offset / Shadow offset in pixels
    'compass_circle_width': 12, # İşaretçi çemberi boyutu / Pointer circle size
    
    # Progress bar dolgu / Progress bar fill
    'progress_bar_min_width': 6,  # Minimum genişlik / Minimum width
}

# Elevation profile vertical scaling - <1.0 reduces visual steepness (1.0 = true scale)
# Yükseklik profili dikey ölçekleme - <1.0 görsel dikliği azaltır (1.0 = gerçek ölçek)
ADVANCED_CONFIG['elevation_vertical_scale'] = 0.6

# ==================== NOT: HUD_CONFIG config.py'YE TAŞINDI ====================
# ==================== NOTE: HUD_CONFIG MOVED TO config.py ====================
"""
HUD_CONFIG artık config.py'de tema bazlı olarak ayarlanıyor
HUD_CONFIG is now set theme-based in config.py
"""

# ==================== DOĞRULAMA VE HATA KONTROL ====================
# ==================== VALIDATION AND ERROR CHECKING ====================
"""
Parametreleri doğrula ve normalize et
Validate and normalize parameters
"""
def validate_advanced_config():
    """
    Gelişmiş konfigürasyon parametrelerinin geçerli olup olmadığını kontrol et
    Check if advanced configuration parameters are valid
    """
    errors = []
    
    # Heart Rate zone'ları kontrol et (sıralı olmalı) / Check Heart Rate zones (should be ordered)
    zone_maxes = [HR_ZONES[i]['max'] for i in range(1, 6)]
    if zone_maxes != sorted(zone_maxes):
        errors.append("HR_ZONES max değerleri sırasız / HR_ZONES max values are not ordered")
    
    # Power config kontrolü / Power config check
    for key in ['rider_weight_kg', 'bike_weight_kg']:
        if POWER_CONFIG[key] <= 0:
            errors.append(f"POWER_CONFIG['{key}'] = {POWER_CONFIG[key]} (pozitif olmalı / must be positive)")
    
    # HUD config kontrolü / HUD config check
    if not (0.0 <= HUD_CONFIG['curve_strength'] <= 1.0):
        errors.append(f"HUD_CONFIG['curve_strength'] = {HUD_CONFIG['curve_strength']} (0-1 aralığında olmalı / must be in 0-1 range)")
    
    if errors:
        print("\n⚠️  GELİŞMİŞ KONFİGÜRASYON UYARILARI / ADVANCED CONFIGURATION WARNINGS:")
        for err in errors:
            print(f"   • {err}")
    
    return len(errors) == 0

# Unit conversion factors / Birim dönüşüm faktörleri
UNIT_CONVERSIONS = {
    'metric': {
        'distance': 1.0,        # km
        'altitude': 1.0,        # m
        'speed': 1.0,           # km/h
        'gradient': 1.0,        # %
        'cadence': 1.0,         # rpm
        'power': 1.0,           # watts
    },
    'imperial': {
        'distance': 0.621371,   # km to miles
        'altitude': 3.28084,    # m to feet
        'speed': 0.621371,      # km/h to mph
        'gradient': 1.0,        # % remains same
        'cadence': 1.0,         # rpm remains same
        'power': 1.0,           # watts remains same
    }
}

# Unit labels for display / Görüntüleme için birim etiketleri
UNIT_LABELS = {
    'metric': {
        'distance': 'km',
        'altitude': 'm',
        'speed': 'km/h',
        'gradient': '%',
        'cadence': 'rpm',
        'power': 'W',
    },
    'imperial': {
        'distance': 'mi',
        'altitude': 'ft',
        'speed': 'mph',
        'gradient': '%',
        'cadence': 'rpm',
        'power': 'W',
    }
}

# Başlangıçta doğrula / Validate at startup
if __name__ == "__main__":
    print("📋 Gelişmiş konfigürasyon dosyası doğrulanıyor... / Validating advanced configuration file...")
    if validate_advanced_config():
        print("✅ Tüm gelişmiş ayarlar geçerli! / All advanced settings are valid!")
    else:
        print("❌ Gelişmiş ayarlarınızı kontrol edin / Check your advanced settings")