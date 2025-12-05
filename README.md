# 🚴 VeloMetrics - Professional Sports Video Analytics

Transform your cycling videos into professional vlogs with GPS data overlay, heart rate zones, and dynamic metrics visualization.

> ⚠️ **Beta Version:** This is an amateur project under active development. Feedback and contributions are welcome to improve the tool!

---

## 📹 Preview

https://imgur.com/a/1vda6qv

---

## ✨ Features

- ✅ GPX Track Synchronization
- ✅ Heart Rate Zones (5-zone system)
- ✅ Dynamic Widgets (speed, altitude, cadence, distance, gradient)
- ✅ Rotating Map
- ✅ Elevation Profile Chart
- ✅ Multiple Themes
- ✅ 100% Modular

---

## 🚀 Quick Start

### Prerequisites
- Your video file (MP4, MOV, AVI, etc.)
- GPX file from your GPS device
- Podman or Docker installed

### Install Podman

**Download and install Podman:**
- Windows/Mac/Linux: https://podman.io/getting-started/installation

**Verify installation:**
```bash
podman --version
```

### Step 1: Prepare Files

```bash
# Copy your files to project folder
cp your_video.mp4 VeloMetrics/
cp your_route.gpx VeloMetrics/
cd VeloMetrics
```

### Step 2: Edit config.py

```python
GPX_DOSYASI = "your_route.gpx"
VIDEO_DOSYASI = "your_video.mp4"
ZAMAN_OFFSET_SANIYE = 0  # GPS time offset in seconds
DEMO_MODU = True         # Test with first 30 seconds
```

### Step 3: Build and Run

**Using Podman:**
```bash
podman build -t velometrics .
podman run --rm -v "$(pwd):/app:rw,z" --userns=keep-id velometrics python3 video_renderer.py
```

**Using Docker:**
```bash
docker build -t velometrics .
docker run --rm -v "$(pwd):/app" velometrics python3 video_renderer.py
```

---

## ⚙️ Configuration

### Theme Selection

Choose your HUD theme in `config.py`:

```python
SELECTED_THEME = 'sport'  # Choose one below
```

**Available Themes:**
- `'classic'` - Glass effect classic (default)
- `'minimal'` - Background off, white text only
- `'neon'` - Bright neon colors, flat design
- `'retro'` - 80s style retro colors
- `'sport'` - Sports themed racing colors
- `'performance'` - Optimized for maximum render speed

### Widget Control

Enable/disable widgets:

```python
WIDGETS_ENABLED = {
    'altitude': True,           # Elevation
    'distance': True,           # Total distance
    'heart_rate': True,         # Heart rate + zones
    'speed': True,              # Current speed
    'gradient': True,           # Slope/gradient
    'cadence': True,            # Pedaling cadence
    'elevation_profile': True,  # Elevation chart
    'route_map': True,          # GPS map
    'progress_bar': True,       # Progress indicator
}
```

### User Settings

```python
USER_AGE = 35                   # For HR zones calculation
RIDER_WEIGHT_KG = 75            # Your weight
BIKE_WEIGHT_KG = 10             # Bike weight
```

### Time Synchronization

```python
# If GPS starts BEFORE video:
ZAMAN_OFFSET_SANIYE = 430   # GPS starts 430 seconds before video

# If GPS starts AFTER video:
ZAMAN_OFFSET_SANIYE = -120  # GPS starts 120 seconds after video (use negative)
```

---

## 🔧 Troubleshooting

### "GPX file not found"
- Check filename matches exactly
- Ensure file is in project folder

### "Video file not found"
- Verify video file location
- Check filename spelling

### Rendering too slow
```python
DEMO_MODU = True  # Test with 30 seconds first
```

### GPS data not syncing
```python
# If GPS starts before video (positive value):
ZAMAN_OFFSET_SANIYE = 420   # GPS starts 7 minutes before video

# If GPS starts after video (negative value):
ZAMAN_OFFSET_SANIYE = -180  # GPS starts 3 minutes after video
```

---

## 📁 File Structure

```
VeloMetrics/
├── config.py              # All settings (START HERE)
├── data_handler.py        # GPX parser
├── utils.py               # Helper functions
├── widgets.py             # Widget rendering
├── video_renderer.py      # Main render (RUN THIS)
├── themes.py              # Theme definitions
├── advanced_config.py     # Advanced settings
├── Dockerfile             # Container config
└── requirements.txt       # Dependencies
```

---

## 💡 Tips

1. **Always test with demo mode first**
   ```python
   DEMO_MODU = True
   ```

2. **Adjust HR zones to your fitness level**
   ```python
   USER_AGE = 35  # Auto-calculated zones
   ```

3. **Disable unused widgets for faster rendering**
   ```python
   WIDGETS_ENABLED['elevation_profile'] = False
   ```

---

## 📄 License

MIT License - Free for personal and commercial use.

---

## 🔗 Links

- **GitHub:** https://github.com/kocercan/VeloMetrics
- **Strava:** https://www.strava.com/athletes/30187784

## 💬 Feedback

This is a beta version and your feedback helps improve VeloMetrics! Please report bugs, suggest features, or share your experience via GitHub Issues.

---

**Made with ❤️ for the cycling community** 🚴♂️🎥
