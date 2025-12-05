# ================================================================
#  HUD TEMA SİSTEMİ - 5 FARKLI TEMA
#  HUD THEME SYSTEM - 5 DIFFERENT THEMES
# ================================================================

# Tema 1: CLASSIC (Varsayılan - Cam efektli, beyaz yazı)
# Theme 1: CLASSIC (Default - Glass effect, white text)
THEME_CLASSIC = {
    'name': 'Classic Glass',
    'description': 'Cam efektli klasik HUD / Glass effect classic HUD',
    'panel_bg_enabled': True,
    'curve_enabled': True,   # Klasik temada eğri var / Curves enabled in classic theme
    'font_style': 'modern',  # Modern, okunabilir font / Modern, readable font
    'icon_style': 'rounded', # Yuvarlatılmış ikonlar / Rounded icons
    'colors': {
        # Arka plan ve cam efektleri / Background and glass effects
        'glass': (30, 30, 30),              # Koyu gri / Dark gray
        'glass_light': (50, 50, 50),        # Açık gri / Light gray
        'glass_dark': (15, 15, 15),         # Çok koyu gri / Very dark gray
        'glass_highlight': (85, 85, 85),    # Üst highlight / Top highlight
        'glass_shadow': (45, 45, 45),       # Alt shadow / Bottom shadow
        
        # Metin renkleri / Text colors
        'text_main': (255, 255, 255),       # Beyaz - ana değerler / White - main values
        'text_sub': (160, 160, 160),        # Gri - başlıklar ve birimler / Gray - titles and units
        
        # Vurgu ve aksesuar / Accent and accessories
        'accent': (0, 200, 255),            # Sarı (neon) - vurgu rengi / Yellow (neon) - accent color
        'border_subtle': (70, 70, 70),      # Hafif border rengi / Subtle border color
        
        # Parametreler - her widget'ın kendi rengi / Parameters - each widget's own color
        'altitude': (100, 180, 255),        # Turuncu - yükseklik / Orange - altitude
        'distance': (255, 180, 50),         # Mavi - mesafe / Blue - distance
        'speed': (80, 255, 80),             # Yeşil - hız / Green - speed
        'gradient': (150, 100, 255),        # Mor - eğim / Purple - gradient
        'cadence': (255, 150, 100),         # Turkuaz - kadans / Turquoise - cadence
        'power': (255, 0, 255),             # Magenta - güç / Magenta - power
        
        # Harita renkleri / Map colors
        'map_path': (120, 120, 120),        # Gri - geçmiş rota / Gray - past route
        'map_path_front': (200, 200, 200),  # Açık gri - gelecek rota / Light gray - future route
        'map_active': (0, 215, 255),        # Sarı - aktif konum / Yellow - active position
        
        # Yükseklik grafiği - eğim renklendirme / Elevation chart - gradient coloring
        'ele_low': (80, 200, 80),           # Yeşil - düşük eğim / Green - low gradient
        'ele_mid': (80, 220, 255),          # Turkuaz - orta eğim / Turquoise - medium gradient
        'ele_high': (80, 80, 255),          # Kırmızı - yüksek eğim / Red - high gradient
        
        # Danger/uyarı / Danger/warning
        'danger': (50, 50, 255),            # Kırmızı uyarı / Red warning
        
        # Heart Rate Zone renkleri / Heart Rate Zone colors
        'zone1': (200, 150, 100),           # Zone 1: Mavi-Gri / Blue-Gray
        'zone2': (100, 200, 100),           # Zone 2: Yeşil / Green
        'zone3': (50, 220, 220),            # Zone 3: Sarı / Yellow
        'zone4': (50, 150, 255),            # Zone 4: Turuncu / Orange
        'zone5': (50, 50, 255),             # Zone 5: Kırmızı / Red
    },
    'opacity': {
        'panel_bg_alpha': 0.7,
        'panel_bg_alpha_large': 0.75,
        'icon_glow_alpha': 0.12,
        'heart_glow_alpha': 0.25,
        'elevation_fill_alpha': 0.3,
    }
}

# Tema 2: MINIMAL (Arka plan kapalı, sadece beyaz yazı)
# Theme 2: MINIMAL (Background disabled, white text only)
THEME_MINIMAL = {
    'name': 'Minimal Clean',
    'description': 'Arka plan kapalı, temiz görünüm / Background disabled, clean look',
    'panel_bg_enabled': False,
    'curve_enabled': False,  # Minimal temada eğri yok / No curves in minimal theme
    'font_style': 'clean',   # Temiz, basit font / Clean, simple font
    'icon_style': 'minimal', # Basit, çizgisel ikonlar / Simple, linear icons
    'colors': {
        # Arka plan ve cam efektleri (kullanılmaz) / Background and glass effects (not used)
        'glass': (0, 0, 0),
        'glass_light': (0, 0, 0),
        'glass_dark': (0, 0, 0),
        'glass_highlight': (0, 0, 0),
        'glass_shadow': (0, 0, 0),
        
        # Metin renkleri / Text colors
        'text_main': (255, 255, 255),       # Beyaz - ana değerler / White - main values
        'text_sub': (200, 200, 200),        # Açık gri - başlıklar / Light gray - titles
        
        # Vurgu ve aksesuar / Accent and accessories
        'accent': (255, 255, 255),          # Beyaz vurgu / White accent
        'border_subtle': (100, 100, 100),   # Hafif border / Subtle border
        
        # Parametreler - monokrom beyaz / Parameters - monochrome white
        'altitude': (255, 255, 255),        # Beyaz / White
        'distance': (255, 255, 255),        # Beyaz / White
        'speed': (255, 255, 255),           # Beyaz / White
        'gradient': (255, 255, 255),        # Beyaz / White
        'cadence': (255, 255, 255),         # Beyaz / White
        'power': (255, 255, 255),           # Beyaz / White
        
        # Harita renkleri / Map colors
        'map_path': (150, 150, 150),        # Gri rota / Gray route
        'map_path_front': (200, 200, 200),  # Açık gri gelecek / Light gray future
        'map_active': (255, 255, 255),      # Beyaz aktif / White active
        
        # Yükseklik grafiği / Elevation chart
        'ele_low': (200, 200, 200),         # Açık gri / Light gray
        'ele_mid': (255, 255, 255),         # Beyaz / White
        'ele_high': (255, 255, 255),        # Beyaz / White
        
        # Danger/uyarı / Danger/warning
        'danger': (255, 255, 255),          # Beyaz / White
        
        # Heart Rate Zone renkleri / Heart Rate Zone colors
        'zone1': (255, 255, 255),           # Beyaz / White
        'zone2': (255, 255, 255),           # Beyaz / White
        'zone3': (255, 255, 255),           # Beyaz / White
        'zone4': (255, 255, 255),           # Beyaz / White
        'zone5': (255, 255, 255),           # Beyaz / White
    },
    'opacity': {
        'panel_bg_alpha': 0.0,              # Arka plan kapalı / Background disabled
        'panel_bg_alpha_large': 0.0,        # Büyük arka planlar kapalı / Large backgrounds disabled
        'icon_glow_alpha': 0.0,             # Glow kapalı / Glow disabled
        'heart_glow_alpha': 0.0,            # Kalp glow kapalı / Heart glow disabled
        'elevation_fill_alpha': 0.0,        # Fill kapalı / Fill disabled
    }
}

# Tema 3: NEON (Parlak neon renkler, flat tasarım)
# Theme 3: NEON (Bright neon colors, flat design)
THEME_NEON = {
    'name': 'Neon Flat',
    'description': 'Parlak neon renkler, flat tasarım / Bright neon colors, flat design',
    'panel_bg_enabled': True,
    'curve_enabled': False,  # Flat tasarımda eğri yok / No curves in flat design
    'font_style': 'bold',    # Kalın, belirgin font / Bold, prominent font
    'icon_style': 'geometric', # Geometrik, keskin ikonlar / Geometric, sharp icons
    'colors': {
        # Arka plan ve cam efektleri / Background and glass effects
        'glass': (20, 20, 40),              # Koyu mavi / Dark blue
        'glass_light': (30, 30, 60),        # Açık koyu mavi / Light dark blue
        'glass_dark': (10, 10, 20),         # Çok koyu mavi / Very dark blue
        'glass_highlight': (40, 40, 80),    # Mavi highlight / Blue highlight
        'glass_shadow': (15, 15, 30),       # Mavi shadow / Blue shadow
        
        # Metin renkleri / Text colors
        'text_main': (255, 255, 255),       # Beyaz / White
        'text_sub': (200, 200, 255),        # Açık mavi / Light blue
        
        # Vurgu ve aksesuar / Accent and accessories
        'accent': (255, 0, 255),            # Magenta vurgu / Magenta accent
        'border_subtle': (100, 100, 200),   # Mavi border / Blue border
        
        # Parametreler - neon renkler / Parameters - neon colors
        'altitude': (0, 255, 255),          # Cyan - yükseklik / Cyan - altitude
        'distance': (255, 255, 0),          # Sarı - mesafe / Yellow - distance
        'speed': (0, 255, 0),               # Yeşil - hız / Green - speed
        'gradient': (255, 0, 255),          # Magenta - eğim / Magenta - gradient
        'cadence': (255, 128, 0),           # Turuncu - kadans / Orange - cadence
        'power': (0, 255, 255),             # Sarı - güç / Yellow - power
        
        # Harita renkleri / Map colors
        'map_path': (100, 100, 200),        # Mavi rota / Blue route
        'map_path_front': (150, 150, 255),  # Açık mavi gelecek / Light blue future
        'map_active': (255, 255, 0),        # Sarı aktif / Yellow active
        
        # Yükseklik grafiği / Elevation chart
        'ele_low': (255, 0, 255),           # Magenta / Magenta
        'ele_mid': (0, 255, 255),           # Cyan / Cyan
        'ele_high': (255, 255, 0),          # Sarı / Yellow
        
        # Danger/uyarı / Danger/warning
        'danger': (255, 0, 0),              # Kırmızı / Red
        
        # Heart Rate Zone renkleri / Heart Rate Zone colors
        'zone1': (0, 255, 255),             # Cyan
        'zone2': (0, 255, 0),               # Yeşil / Green
        'zone3': (255, 255, 0),             # Sarı / Yellow
        'zone4': (255, 128, 0),             # Turuncu / Orange
        'zone5': (255, 0, 0),               # Kırmızı / Red
    },
    'opacity': {
        'panel_bg_alpha': 0.8,
        'panel_bg_alpha_large': 0.85,
        'icon_glow_alpha': 0.4,
        'heart_glow_alpha': 0.5,
        'elevation_fill_alpha': 0.6,  # Daha opak elevation fill / More opaque elevation fill
    }
}

# Tema 4: RETRO (80'ler tarzı renkler)
# Theme 4: RETRO (80s style colors)
THEME_RETRO = {
    'name': 'Retro 80s',
    'description': '80\'ler tarzı retro renkler / 80s style retro colors',
    'panel_bg_enabled': True,
    'curve_enabled': True,   # Retro temada eğri var / Curves enabled in retro theme
    'font_style': 'retro',   # Retro, pixelated font / Retro, pixelated font
    'icon_style': 'retro',   # 80'ler tarzı ikonlar / 80s style icons
    'colors': {
        # Arka plan ve cam efektleri / Background and glass effects
        'glass': (40, 20, 60),              # Mor arka plan / Purple background
        'glass_light': (60, 30, 90),        # Açık mor / Light purple
        'glass_dark': (20, 10, 30),         # Koyu mor / Dark purple
        'glass_highlight': (80, 40, 120),   # Mor highlight / Purple highlight
        'glass_shadow': (30, 15, 45),       # Mor shadow / Purple shadow
        
        # Metin renkleri / Text colors
        'text_main': (255, 255, 255),       # Beyaz / White
        'text_sub': (255, 200, 255),        # Açık pembe / Light pink
        
        # Vurgu ve aksesuar / Accent and accessories
        'accent': (255, 0, 255),            # Magenta vurgu / Magenta accent
        'border_subtle': (150, 100, 200),   # Mor border / Purple border
        
        # Parametreler - retro renkler / Parameters - retro colors
        'altitude': (255, 100, 255),        # Magenta - yükseklik / Magenta - altitude
        'distance': (100, 255, 255),        # Cyan - mesafe / Cyan - distance
        'speed': (255, 255, 100),           # Sarı - hız / Yellow - speed
        'gradient': (255, 100, 100),        # Pembe - eğim / Pink - gradient
        'cadence': (100, 255, 100),         # Yeşil - kadans / Green - cadence
        'power': (0, 200, 255),             # Turuncu - güç / Orange - power
        
        # Harita renkleri / Map colors
        'map_path': (150, 100, 200),        # Mor rota / Purple route
        'map_path_front': (200, 150, 255),  # Açık mor gelecek / Light purple future
        'map_active': (255, 255, 100),      # Sarı aktif / Yellow active
        
        # Yükseklik grafiği / Elevation chart
        'ele_low': (100, 255, 100),         # Yeşil / Green
        'ele_mid': (255, 255, 100),         # Sarı / Yellow
        'ele_high': (255, 100, 255),        # Magenta
        
        # Danger/uyarı / Danger/warning
        'danger': (255, 100, 100),          # Pembe / Pink
        
        # Heart Rate Zone renkleri / Heart Rate Zone colors
        'zone1': (100, 255, 255),           # Cyan
        'zone2': (100, 255, 100),           # Yeşil / Green
        'zone3': (255, 255, 100),           # Sarı / Yellow
        'zone4': (255, 150, 100),           # Turuncu / Orange
        'zone5': (255, 100, 255),           # Magenta
    },
    'opacity': {
        'panel_bg_alpha': 0.75,
        'panel_bg_alpha_large': 0.8,
        'icon_glow_alpha': 0.3,
        'heart_glow_alpha': 0.4,
        'elevation_fill_alpha': 0.35,
    }
}

# Tema 5: SPORT (Spor temalı renkler - kırmızı, beyaz, siyah)
# Theme 5: SPORT (Sports themed racing colors - red, white, black)
THEME_SPORT = {
    'name': 'Sport Racing',
    'description': 'Spor temalı yarış renkleri / Sports themed racing colors',
    'panel_bg_enabled': True,
    'curve_enabled': True,   # Spor temada eğri var / Curves enabled in sport theme
    'font_style': 'sport',   # Spor, dinamik font / Sport, dynamic font
    'icon_style': 'sport',   # Spor temalı ikonlar / Sport themed icons
    'colors': {
        # Arka plan ve cam efektleri / Background and glass effects
        'glass': (20, 20, 20),              # Siyah arka plan / Black background
        'glass_light': (40, 40, 40),        # Koyu gri / Dark gray
        'glass_dark': (10, 10, 10),         # Çok siyah / Very black
        'glass_highlight': (60, 60, 60),    # Gri highlight / Gray highlight
        'glass_shadow': (5, 5, 5),          # Siyah shadow / Black shadow
        
        # Metin renkleri / Text colors
        'text_main': (255, 255, 255),       # Beyaz / White
        'text_sub': (200, 200, 200),        # Açık gri / Light gray
        
        # Vurgu ve aksesuar / Accent and accessories
        'accent': (0, 0, 255),              # Kırmızı vurgu / Red accent
        'border_subtle': (100, 100, 100),   # Gri border / Gray border
        
        # Parametreler - spor renkler / Parameters - sport colors
        'altitude': (0, 100, 255),          # Kırmızı - yükseklik / Red - altitude
        'distance': (255, 255, 255),        # Beyaz - mesafe / White - distance
        'speed': (0, 255, 0),               # Yeşil - hız / Green - speed
        'gradient': (0, 150, 255),          # Turuncu - eğim / Orange - gradient
        'cadence': (0, 255, 255),           # Sarı - kadans / Yellow - cadence
        'power': (0, 100, 255),             # Kırmızı-Turuncu - güç / Red-Orange - power
        
        # Harita renkleri / Map colors
        'map_path': (100, 100, 100),        # Gri rota / Gray route
        'map_path_front': (150, 150, 150),  # Açık gri gelecek / Light gray future
        'map_active': (0, 0, 255),          # Kırmızı aktif / Red active
        
        # Yükseklik grafiği / Elevation chart
        'ele_low': (0, 255, 0),             # Yeşil / Green
        'ele_mid': (0, 255, 255),           # Sarı / Yellow
        'ele_high': (0, 0, 255),            # Kırmızı / Red
        
        # Danger/uyarı / Danger/warning
        'danger': (0, 0, 255),              # Kırmızı / Red
        
        # Heart Rate Zone renkleri / Heart Rate Zone colors
        'zone1': (200, 200, 200),           # Gri / Gray
        'zone2': (0, 255, 0),               # Yeşil / Green
        'zone3': (0, 255, 255),             # Sarı / Yellow
        'zone4': (0, 150, 255),             # Turuncu / Orange
        'zone5': (0, 0, 255),               # Kırmızı / Red
    },
    'opacity': {
        'panel_bg_alpha': 0.85,
        'panel_bg_alpha_large': 0.9,
        'icon_glow_alpha': 0.2,
        'heart_glow_alpha': 0.3,
        'elevation_fill_alpha': 0.25,
    }
}

# Tema 6: PERFORMANCE (Performans odaklı - hızlı render)
# Theme 6: PERFORMANCE (Performance focused - fast render)
THEME_PERFORMANCE = {
    'name': 'Performance Fast',
    'description': 'Maksimum hız için optimize edilmiş / Optimized for maximum speed',
    'panel_bg_enabled': False,  # Arka plan yok / No backgrounds
    'curve_enabled': False,     # Eğri yok / No curves
    'font_style': 'performance', # En basit font / Simplest font
    'icon_style': 'performance', # En basit ikonlar / Simplest icons
    'colors': {
        # Minimal renkler / Minimal colors
        'glass': (0, 0, 0),
        'glass_light': (0, 0, 0),
        'glass_dark': (0, 0, 0),
        'glass_highlight': (0, 0, 0),
        'glass_shadow': (0, 0, 0),
        
        # Sadece beyaz metin / White text only
        'text_main': (255, 255, 255),
        'text_sub': (200, 200, 200),
        
        # Minimal vurgu / Minimal accent
        'accent': (255, 255, 255),
        'border_subtle': (100, 100, 100),
        
        # Monokrom parametreler / Monochrome parameters
        'altitude': (255, 255, 255),
        'distance': (255, 255, 255),
        'speed': (255, 255, 255),
        'gradient': (255, 255, 255),
        'cadence': (255, 255, 255),
        'power': (255, 255, 255),
        
        # Basit harita / Simple map
        'map_path': (150, 150, 150),
        'map_path_front': (200, 200, 200),
        'map_active': (255, 255, 255),
        
        # Basit elevation / Simple elevation
        'ele_low': (200, 200, 200),
        'ele_mid': (255, 255, 255),
        'ele_high': (255, 255, 255),
        
        'danger': (255, 255, 255),
        
        # Monokrom zones / Monochrome zones
        'zone1': (255, 255, 255),
        'zone2': (255, 255, 255),
        'zone3': (255, 255, 255),
        'zone4': (255, 255, 255),
        'zone5': (255, 255, 255),
    },
    'opacity': {
        'panel_bg_alpha': 0.0,      # Tüm arka planlar kapalı / All backgrounds off
        'panel_bg_alpha_large': 0.0,
        'icon_glow_alpha': 0.0,     # Tüm efektler kapalı / All effects off
        'heart_glow_alpha': 0.0,
        'elevation_fill_alpha': 0.0,
    }
}

# Tüm temalar / All themes
THEMES = {
    'classic': THEME_CLASSIC,
    'minimal': THEME_MINIMAL,
    'neon': THEME_NEON,
    'retro': THEME_RETRO,
    'sport': THEME_SPORT,
    'performance': THEME_PERFORMANCE,
}

def get_theme(theme_name):
    """
    Tema adına göre tema döndür / Return theme by name
    """
    if theme_name not in THEMES:
        print(f"⚠️  Tema bulunamadı: {theme_name}. Varsayılan tema kullanılıyor.")
        print(f"⚠️  Theme not found: {theme_name}. Using default theme.")
        return THEMES['classic']
    return THEMES[theme_name]

# ==================== FONT AYARLARI TEMA BAZINDA ====================
# ==================== THEME-BASED FONT SETTINGS ====================

FONT_CONFIGS = {
    'modern': {
        'font_family_preferred': ['Roboto-Bold.ttf', 'DejaVuSans-Bold.ttf'],
        'title_size': 0.40,
        'value_size': 0.92,
        'unit_size': 0.48,
        'small_size': 0.38,
        'title_thickness': 1.2,
        'value_thickness': 1.6,
        'unit_thickness': 0.6,
        'small_thickness': 0.6,
    },
    'clean': {
        'font_family_preferred': ['Inter-Regular.ttf', 'Arial.ttf'],
        'title_size': 0.35,
        'value_size': 0.85,
        'unit_size': 0.42,
        'small_size': 0.32,
        'title_thickness': 1.0,
        'value_thickness': 1.4,
        'unit_thickness': 0.5,
        'small_thickness': 0.5,
    },
    'bold': {
        'font_family_preferred': ['Montserrat-Black.ttf', 'Arial-Bold.ttf'],
        'title_size': 0.45,
        'value_size': 1.0,
        'unit_size': 0.52,
        'small_size': 0.42,
        'title_thickness': 1.5,
        'value_thickness': 2.0,
        'unit_thickness': 0.8,
        'small_thickness': 0.8,
    },
    'retro': {
        'font_family_preferred': ['Orbitron-Bold.ttf', 'Courier-Bold.ttf'],
        'title_size': 0.42,
        'value_size': 0.95,
        'unit_size': 0.45,
        'small_size': 0.35,
        'title_thickness': 1.3,
        'value_thickness': 1.8,
        'unit_thickness': 0.7,
        'small_thickness': 0.7,
    },
    'sport': {
        'font_family_preferred': ['Rajdhani-Bold.ttf', 'Impact.ttf'],
        'title_size': 0.38,
        'value_size': 0.88,
        'unit_size': 0.46,
        'small_size': 0.36,
        'title_thickness': 1.4,
        'value_thickness': 1.9,
        'unit_thickness': 0.7,
        'small_thickness': 0.7,
    },
    'performance': {
        'font_family_preferred': ['Arial.ttf'],
        'title_size': 0.32,         # Küçük boyutlar / Small sizes
        'value_size': 0.75,         # Hızlı render / Fast render
        'unit_size': 0.38,
        'small_size': 0.28,
        'title_thickness': 1.0,     # İnce çizgiler / Thin lines
        'value_thickness': 1.2,     # Minimum kalınlık / Minimum thickness
        'unit_thickness': 0.8,
        'small_thickness': 0.8,
    }
}

# ==================== İKON STYL AYARLARI ====================
# ==================== ICON STYLE SETTINGS ====================

ICON_STYLES = {
    'rounded': {
        'corner_radius': 3,
        'line_width': 2,
        'fill_style': 'solid',
        'glow_enabled': True,
    },
    'minimal': {
        'corner_radius': 0,
        'line_width': 1,
        'fill_style': 'outline',
        'glow_enabled': False,
    },
    'geometric': {
        'corner_radius': 0,
        'line_width': 3,
        'fill_style': 'solid',
        'glow_enabled': True,
    },
    'retro': {
        'corner_radius': 1,
        'line_width': 2,
        'fill_style': 'pixelated',
        'glow_enabled': True,
    },
    'sport': {
        'corner_radius': 2,
        'line_width': 3,
        'fill_style': 'solid',
        'glow_enabled': True,
    },
    'performance': {
        'corner_radius': 0,         # Köşe yok / No corners
        'line_width': 1,            # En ince çizgi / Thinnest line
        'fill_style': 'outline',    # Sadece çizgi / Outline only
        'glow_enabled': False,      # Efekt yok / No effects
    }
}

def get_font_config(font_style):
    """
    Font stiline göre font ayarlarını döndür / Return font settings by font style
    """
    if font_style not in FONT_CONFIGS:
        print(f"⚠️  Font stili bulunamadı: {font_style}. Varsayılan kullanılıyor.")
        return FONT_CONFIGS['modern']
    return FONT_CONFIGS[font_style]

def get_icon_style(icon_style):
    """
    İkon stiline göre ikon ayarlarını döndür / Return icon settings by icon style
    """
    if icon_style not in ICON_STYLES:
        print(f"⚠️  İkon stili bulunamadı: {icon_style}. Varsayılan kullanılıyor.")
        return ICON_STYLES['rounded']
    return ICON_STYLES[icon_style]

def list_themes():
    """
    Mevcut temaları listele / List available themes
    """
    print("\n🎨 Mevcut Temalar / Available Themes:")
    for key, theme in THEMES.items():
        bg_status = "Arka plan VAR" if theme['panel_bg_enabled'] else "Arka plan YOK"
        bg_status_en = "Background ON" if theme['panel_bg_enabled'] else "Background OFF"
        curve_status = "Eğri VAR" if theme.get('curve_enabled', True) else "Eğri YOK"
        curve_status_en = "Curves ON" if theme.get('curve_enabled', True) else "Curves OFF"
        print(f"  • {key}: {theme['name']} - {theme['description']}")
        print(f"    {bg_status} / {bg_status_en}, {curve_status} / {curve_status_en}")
        print(f"    Font: {theme.get('font_style', 'modern')}, İkon: {theme.get('icon_style', 'rounded')}")
    print()