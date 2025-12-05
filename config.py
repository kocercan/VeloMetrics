# ================================================================
#  PRO VERSİYON v5 - KULLANICI DOSTU KONFİGÜRASYON
#  PRO VERSION v5 - USER FRIENDLY CONFIGURATION
# ================================================================
#  🚀 HIZLI BAŞLANGIÇ / QUICK START:
#  1. Dosya yollarını ayarla / Set file paths
#  2. Tema seç / Choose theme  
#  3. Widget'ları aç/kapat / Enable/disable widgets
#  4. python video_renderer.py çalıştır / run python video_renderer.py
# ================================================================

# Tema sistemi ve gelişmiş ayarları import et / Import theme system and advanced settings
from themes import THEMES, get_theme, list_themes
from advanced_config import *
from messages import print_message, print_section, print_success, print_error, print_info

# ==================== 1. DOSYA YÖNETİMİ (ÖNEMLİ!) ====================
# ==================== 1. FILE MANAGEMENT (IMPORTANT!) ====================
"""
🎯 BURADAN BAŞLA! Kendi dosya yollarını gir
🎯 START HERE! Enter your own file paths
"""
GPX_DOSYASI = "ornek.gpx"                    # GPX iz dosyası / GPX track file
VIDEO_DOSYASI = "VID_20251202_131330.mp4"     # Video dosyası / Video file  
# Otomatik tarih-zaman eklemeli çıkış dosyası / Auto date-time output file
import datetime
base_output_name = "vlog_PRO_v5"
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
CIKTI_DOSYASI = f"{base_output_name}_{timestamp}.mp4"  # Çıkış dosyası / Output file

# ==================== 2. TEMA SEÇİMİ (ÖNEMLİ!) ====================
# ==================== 2. THEME SELECTION (IMPORTANT!) ====================
"""
🎨 HUD TEMA SEÇ / CHOOSE HUD THEME:
- 'classic': Cam efektli klasik (varsayılan) / Glass effect classic (default)
- 'minimal': Arka plan kapalı, sadece beyaz yazı / Background off, white text only
- 'neon': Parlak neon renkler, flat tasarım / Bright neon colors, flat design
- 'retro': 80'ler tarzı retro renkler / 80s style retro colors  
- 'sport': Spor temalı yarış renkleri / Sports themed racing colors
- 'performance': Maksimum render hızı için optimize / Optimized for maximum render speed

Mevcut temaları görmek için: python -c "from themes import list_themes; list_themes()"
To see available themes: python -c "from themes import list_themes; list_themes()"
"""
SELECTED_THEME = 'sport'  # Tema adını buraya yaz / Write theme name here

# Seçilen temayı yükle / Load selected theme
current_theme = get_theme(SELECTED_THEME)
COLORS = current_theme['colors']
OPACITY = current_theme['opacity']
PANEL_BG_ENABLED = current_theme['panel_bg_enabled']
CURVE_ENABLED = current_theme.get('curve_enabled', True)
FONT_STYLE = current_theme.get('font_style', 'modern')
ICON_STYLE = current_theme.get('icon_style', 'rounded')

# Tema bazlı font ve ikon ayarlarını yükle / Load theme-based font and icon settings
from themes import get_font_config, get_icon_style
theme_font_config = get_font_config(FONT_STYLE)
theme_icon_config = get_icon_style(ICON_STYLE)

# ==================== 3. ZAMAN AYARLARI ====================
# ==================== 3. TIME SETTINGS ====================
"""
⏰ Video ve GPX senkronizasyonu / Video and GPX synchronization
ZAMAN_OFFSET_SANIYE: GPX'in video'dan kaç saniye önceden başladığını belirtir
ZAMAN_OFFSET_SANIYE: How many seconds GPX started before the video
"""
ZAMAN_OFFSET_SANIYE = 430  # saniye / seconds

# ==================== 4. TEST MODU ====================
# ==================== 4. TEST MODE ====================
"""
🧪 Test için kısa video işle / Process short video for testing
"""
DEMO_MODU = True                # True = test modu / True = test mode
DEMO_MODE_SECONDS = 30          # Kaç saniye işle / How many seconds to process
DEMO_START_SECONDS = 0        # Hangi saniyeden başla / Which second to start from

# ==================== 5. WIDGET AÇMA/KAPAMA (ÖNEMLİ!) ====================
# ==================== 5. WIDGET ENABLE/DISABLE (IMPORTANT!) ====================
"""
🎛️ Hangi widget'ları göstermek istiyorsun? / Which widgets do you want to show?
False = widget görünmez / False = widget invisible
True = widget görünür / True = widget visible
"""
WIDGETS_ENABLED = {
    # Sol paneller / Left panels
    'altitude': True,          # Yükseklik / Altitude
    'distance': True,          # Mesafe / Distance  
    'heart_rate': True,        # Kalp atışı + Zone / Heart rate + Zone
    
    # Sağ paneller / Right panels
    'speed': True,             # Hız / Speed
    'gradient': True,          # Eğim / Gradient
    'cadence': True,           # Kadans / Cadence
    'power': True,             # Güç / Power
    
    # Alt widget'lar / Bottom widgets
    'elevation_profile': True, # Eğim grafiği / Elevation chart
    'route_map': True,         # Harita / Map
    'progress_bar': True,      # İlerleme çubuğu / Progress bar
}

# ==================== 6. BİRİM SİSTEMİ ====================
# ==================== 6. UNIT SYSTEM ====================
"""
📏 Metrik mi Imperial mi? / Metric or Imperial?
"""
UNIT_SYSTEM = 'metric'  # 'metric' veya 'imperial' / 'metric' or 'imperial'

# ==================== 6.1. KULLANICI BİLGİLERİ ====================
# ==================== 6.1. USER INFORMATION ====================
"""
👤 Kişisel bilgiler (kalp atış zone'ları ve güç hesaplaması için)
👤 Personal information (for heart rate zones and power calculation)
"""
USER_AGE = 35                    # Yaşınız / Your age
RIDER_WEIGHT_KG = 75             # Ağırlığınız (kg) / Your weight (kg)
BIKE_WEIGHT_KG = 10              # Bisiklet ağırlığı (kg) / Bike weight (kg)

# ==================== 6.2. GÜÇLÜ HESAPLAMA ====================
# ==================== 6.2. POWER CALCULATION ====================
"""
⚡ Strava benzeri güç hesaplaması / Strava-like power calculation
"""
POWER_CONFIG = {
    'rider_weight_kg': RIDER_WEIGHT_KG,
    'bike_weight_kg': BIKE_WEIGHT_KG,
    'cda': 0.35,                # Aerodinamik sürükleme / Aerodynamic drag
    'crr': 0.004,               # Yuvarlanma direnci / Rolling resistance
    'drivetrain_efficiency': 0.97,  # Aktarım verimi / Drivetrain efficiency
    'air_density': 1.225,       # Hava yoğunluğu / Air density
    'wind_speed': 0,            # Rüzgar hızı / Wind speed (m/s)
    'smoothing_window': 5,      # Smoothing penceresi / Smoothing window
    'min_power': 0,             # Min güç / Min power (W)
    'max_power': 1500,          # Max güç / Max power (W)
}

# ==================== 6.3. KALP ATIŞI ZONE'LARI ====================
# ==================== 6.3. HEART RATE ZONES ====================
"""
💓 Yaşa göre otomatik zone hesaplama / Automatic zone calculation by age
"""
def calculate_hr_zones(age):
    """Yaşa göre HR zone'larını hesapla / Calculate HR zones by age"""
    max_hr = 220 - age
    return {
        1: {'min': 0,                    'max': int(max_hr * 0.60), 'name': 'ZONE 1', 'desc': 'Recovery'},
        2: {'min': int(max_hr * 0.60),   'max': int(max_hr * 0.70), 'name': 'ZONE 2', 'desc': 'Endurance'},
        3: {'min': int(max_hr * 0.70),   'max': int(max_hr * 0.80), 'name': 'ZONE 3', 'desc': 'Tempo'},
        4: {'min': int(max_hr * 0.80),   'max': int(max_hr * 0.90), 'name': 'ZONE 4', 'desc': 'Threshold'},
        5: {'min': int(max_hr * 0.90),   'max': 300,               'name': 'ZONE 5', 'desc': 'VO2 Max'},
    }

HR_ZONES = calculate_hr_zones(USER_AGE)

# ==================== 6.4. HAP HARITA AYARLARI ====================
# ==================== 6.4. MAP SETTINGS ====================
"""
🗺️ Harita zoom ve görüntüleme / Map zoom and display
"""
MAP_CONFIG = {
    'zoom_factor': 80000,       # Zoom seviyesi / Zoom level
    'display_range': 200,       # Gösterilen waypoint sayısı / Number of waypoints shown
    'map_radius': None,         # Otomatik hesaplanır / Auto calculated
}

# ==================== 7. FONT AYARLARI (TEMA BAZLI) ====================
# ==================== 7. FONT SETTINGS (THEME-BASED) ====================
"""
🔤 Yazı tipi ve boyut ayarları (seçilen temaya göre otomatik) 
🔤 Font type and size settings (automatic based on selected theme)
"""
FONT_CONFIG = {
    # Tema bazlı font ayarları / Theme-based font settings
    'font_family_preferred': theme_font_config['font_family_preferred'],
    'font_path': None,                 # TTF dosya yolu / TTF file path
    'use_freetype': False,             # TTF kullan / Use TTF
    
    # Font yüzleri / Font faces (büyük değerler için optimize)
    'font_face_title': 'FONT_HERSHEY_SIMPLEX',
    'font_face_value': 'FONT_HERSHEY_TRIPLEX',  # En kalın font - büyük değerler için
    'font_face_unit': 'FONT_HERSHEY_SIMPLEX',
    'font_face_small': 'FONT_HERSHEY_SIMPLEX',

    # Boyutlar (temadan) / Sizes (from theme)
    'title_size': theme_font_config['title_size'],
    'value_size': theme_font_config['value_size'],
    'unit_size': theme_font_config['unit_size'],
    'small_size': theme_font_config['small_size'],

    # Kalınlık (temadan) / Thickness (from theme)
    'title_thickness': theme_font_config['title_thickness'],
    'value_thickness': theme_font_config['value_thickness'],
    'unit_thickness': theme_font_config['unit_thickness'],
    'small_thickness': theme_font_config['small_thickness'],

    # Kontur / Outline
    'outline_enabled': True,        # Kontur çiz / Draw outline
    'outline_color': (0, 0, 0),     # Kontur rengi (BGR) / Outline color (BGR)
    'outline_strength': 0.3,        # Kontur kalınlığı / Outline thickness

    # Kalite / Quality
    'line_type': 'LINE_AA',         # Anti-aliasing
}

# İkon ayarları (tema bazlı) / Icon settings (theme-based)
ICON_CONFIG = theme_icon_config

# ==================== 8. EKRAN DÜZENİ ====================
# ==================== 8. SCREEN LAYOUT ====================
"""
📺 Widget boyutları ve konumları / Widget sizes and positions
"""
# Widget boyutları / Widget sizes
WIDGET_WIDTH_RATIO = 0.16       # Ekran genişliğinin %'si / % of screen width
WIDGET_HEIGHT_RATIO = 0.08      # Ekran yüksekliğinin %'si / % of screen height
WIDGET_MIN_WIDTH = 160          # Minimum genişlik / Minimum width
WIDGET_MIN_HEIGHT = 44          # Minimum yükseklik / Minimum height

# Büyük kutular (harita, eğim) / Large boxes (map, elevation)
BOX_SIZE_RATIO = 0.28           # Ekran boyutunun %'si / % of screen size
BOX_SIZE_MIN = 160              # Minimum kutu boyutu / Minimum box size

# Boşluklar / Spacing
PADDING_RATIO = 0.03            # Kenar boşluğu / Edge padding
PADDING_MIN = 8                 # Minimum kenar boşluğu / Minimum edge padding
GAP_RATIO = 0.01                # Widget arası boşluk / Gap between widgets
GAP_MIN = 6                     # Minimum boşluk / Minimum gap

# Genel ölçekleme / Global scaling
WIDGET_SCALE = 0.8              # Tüm widget'ları küçült/büyüt / Shrink/enlarge all widgets
WIDGET_VERTICAL_SHIFT_RATIO = -0.02  # Widget'ları yukarı/aşağı kaydır / Move widgets up/down
TOP_WIDGET_OFFSET_PX = 55       # Üst widget'lar için ek boşluk / Extra space for top widgets

# İlerleme çubuğu / Progress bar
PROGRESS_BAR_WIDTH_RATIO = 0.35 # Genişlik oranı / Width ratio
PROGRESS_BAR_HEIGHT = 6         # Yükseklik / Height

# ==================== 9. EFEKTLER (TEMA BAZLI) ====================
# ==================== 9. EFFECTS (THEME-BASED) ====================
"""
✨ Görsel efektler (seçilen temaya göre otomatik)
✨ Visual effects (automatic based on selected theme)
"""
# Curved screen efektleri / Curved screen effects
İÇBÜKEY_EFEKT = False          # İçbükey gradient arka planlar / Concave gradient backgrounds
KONVEKS_EFEKT = False          # Video distorsiyon (KALDIRILDI) / Video distortion (REMOVED)

# HUD eğri ayarları (temadan) / HUD curve settings (from theme)
HUD_CONFIG = {
    'unified_hud': True,
    'curve_enabled': CURVE_ENABLED,  # Temaya göre / Based on theme
    'curve_strength': 0.03 if CURVE_ENABLED else 0.0,
    'fade_strength': 2.9,
    'bg_lum_threshold': 90,
    'fast_mode': False,
    'roi_remap': True,
    'hud_downscale': 0.9,
    'hud_update_rate': 15,
    'remap_cache_enabled': True,
    'remap_cache_max_entries': 4,
    'distance_cache_max_entries': 4,
}

# ==================== TEMA BİLGİSİ GÖSTER ====================
# ==================== SHOW THEME INFO ====================
def show_current_theme():
    """Seçili tema bilgisini göster / Show selected theme info"""
    theme = get_theme(SELECTED_THEME)
    bg_status = "ON" if theme['panel_bg_enabled'] else "OFF"
    curve_status = "ON" if theme.get('curve_enabled', True) else "OFF"
    
    print(f"\n🎨 Selected Theme: {SELECTED_THEME}")
    print(f"   📛 Name: {theme['name']}")
    print(f"   📝 Description: {theme['description']}")
    print(f"   🖼️  Background: {bg_status}")
    print(f"   🌊 Curves: {curve_status}")
    print(f"   🔤 Font Style: {theme.get('font_style', 'modern')}")
    print(f"   🎨 Icon Style: {theme.get('icon_style', 'rounded')}")
    
    # Widget durumları / Widget states
    enabled_widgets = [k for k, v in WIDGETS_ENABLED.items() if v]
    disabled_widgets = [k for k, v in WIDGETS_ENABLED.items() if not v]
    
    if enabled_widgets:
        print(f"   ✅ Active Widgets: {', '.join(enabled_widgets)}")
    if disabled_widgets:
        print(f"   ❌ Disabled Widgets: {', '.join(disabled_widgets)}")
    print()

# ==================== DOĞRULAMA ====================
# ==================== VALIDATION ====================
def validate_config():
    """
    Temel konfigürasyon parametrelerini doğrula
    Validate basic configuration parameters
    """
    errors = []
    
    # Tema kontrolü / Theme check
    if SELECTED_THEME not in THEMES:
        errors.append(f"Geçersiz tema / Invalid theme: {SELECTED_THEME}")
    
    # Dosya kontrolü / File check
    import os
    if not os.path.exists(GPX_DOSYASI):
        errors.append(f"GPX dosyası bulunamadı / GPX file not found: {GPX_DOSYASI}")
    if not os.path.exists(VIDEO_DOSYASI):
        errors.append(f"Video dosyası bulunamadı / Video file not found: {VIDEO_DOSYASI}")
    
    # Opacity kontrolü / Opacity check
    for key, val in OPACITY.items():
        if not (0.0 <= val <= 1.0):
            errors.append(f"OPACITY['{key}'] = {val} (0-1 aralığında olmalı / must be in 0-1 range)")
    
    # Font boyut kontrolü / Font size check
    font_sizes = ['title_size', 'value_size', 'unit_size', 'small_size']
    for key in font_sizes:
        val = FONT_CONFIG[key]
        if val <= 0:
            errors.append(f"FONT_CONFIG['{key}'] = {val} (pozitif olmalı / must be positive)")
    
    # Zaman kontrolü / Time check
    if ZAMAN_OFFSET_SANIYE < 0:
        errors.append(f"ZAMAN_OFFSET_SANIYE = {ZAMAN_OFFSET_SANIYE} (negatif olamaz / cannot be negative)")
    
    if errors:
        print("\n⚠️  KONFİGÜRASYON HATALARI / CONFIGURATION ERRORS:")
        for err in errors:
            print(f"   • {err}")
        return False
    
    return True

# ==================== BAŞLANGIÇ KONTROLÜ ====================
# ==================== STARTUP CHECK ====================
if __name__ == "__main__":
    print_section('startup_title')
    
    # Tema bilgisini göster / Show theme info
    show_current_theme()
    
    # Tema ayarlarını göster / Show theme settings
    print(f"\n🎨 Theme loaded: {SELECTED_THEME} ({current_theme['name']})")

    
    # Konfigürasyonu doğrula / Validate configuration
    print_message('config_loading')
    if validate_config():
        print_success('config_valid')
        print("🚀 To start rendering: python video_renderer.py")
    else:
        print_error('config_invalid')
        print("💡 See README.md for help")
    
    print("\n💡 To change theme:")
    print("   SELECTED_THEME = 'theme_name' # in config.py")
    
    print("\n🎨 Available themes:")
    list_themes()
