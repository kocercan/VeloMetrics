# ================================================================
#  GPX VE VERİ İŞLEME MODÜLÜ (data_handler.py)
#  ================================================================
#  İçerik:
#  - GPX dosyası parsing (koordinat, yükseklik, HR, Kadans)
#  - Veri interpolasyon (video frame'lerine uyarla)
#  - Heart Rate Zone hesaplaması
#  - Navigasyon (heading, gradyan, hız)
#  ================================================================

import gpxpy
import numpy as np
from datetime import timedelta
from geopy.distance import geodesic
import math
from config import HR_ZONES, ZAMAN_OFFSET_SANIYE


# ================================================================
#  GPX PARSER
#  ================================================================

def parse_gpx(file_path):
    """
    GPX dosyasını parse et ve waypoint'ler listesini döndür.
    
    Her waypoint'te:
    - Zaman (t)
    - Konum (lat, lon)
    - Yükseklik (ele)
    - Kalp atış hızı (hr) - varsa
    - Kadans (cad) - varsa
    - Kümülatif mesafe (cum_dist)
    
    Args:
        file_path (str): GPX dosyasının yolu
    
    Returns:
        list: Waypoint'ler listesi (dict)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            gpx = gpxpy.parse(f)
    except FileNotFoundError:
        print(f"❌ ERROR: '{file_path}' not found.")
        return []
    
    points = []
    total_dist = 0.0
    prev = None

    # Track'leri ve segment'leri parse et
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                hr = None
                cad = None
                
                # Extension verilerini ara (kalp atış, kadans)
                if point.extensions:
                    for ext in point.extensions:
                        for child in ext:
                            tag_lower = child.tag.lower()
                            
                            # Kalp atış hızı ara
                            if 'hr' in tag_lower:
                                try:
                                    hr = int(child.text)
                                except (ValueError, TypeError):
                                    pass
                            
                            # Kadans ara
                            if 'cad' in tag_lower:
                                try:
                                    cad = int(child.text)
                                except (ValueError, TypeError):
                                    pass
                
                # Mesafe hesapla (segment distance) - expensive geodesic called only once at parse time
                if prev:
                    d = geodesic(
                        (prev['lat'], prev['lon']),
                        (point.latitude, point.longitude)
                    ).meters
                    total_dist += d
                else:
                    d = 0.0
                
                # Waypoint kaydını ekle
                points.append({
                    't': point.time,
                    'lat': point.latitude,
                    'lon': point.longitude,
                    'ele': point.elevation or 0,
                    'hr': hr,
                    'cad': cad,
                    'cum_dist': total_dist,
                    'seg_dist': d
                })
                
                prev = {'lat': point.latitude, 'lon': point.longitude}
    
    if not points:
        print(f"⚠️  Warning: No data found in GPX file!")
        return []
    
    print(f"✅ GPX parsed: {len(points)} waypoints, {total_dist/1000:.2f} km")
    return points


# ================================================================
#  HEART RATE ZONE SİSTEMİ
#  ================================================================

def get_hr_zone(hr):
    """
    Kalp atış hızına göre zone (1-5) belirle.
    
    Zone detayları config.HR_ZONES'de tanımlanmış.
    
    Args:
        hr (float/int): Kalp atış hızı (bpm)
    
    Returns:
        tuple: (zone_number, zone_color, zone_text)
        Örnek: (2, (100, 200, 100), "ZONE 2 - Endurance")
    """
    from config import COLORS
    
    if not hr or hr == 0:
        # Veri yok
        return None, (128, 128, 128), "---"
    
    # Zone'u belirle (min <= hr < max)
    for zone_num in range(1, 6):
        zone_info = HR_ZONES[zone_num]
        if zone_info['min'] <= hr < zone_info['max']:
            zone_color = COLORS[f'zone{zone_num}']
            return zone_num, zone_color, zone_info['name']
    
    # hr >= 300'ün üzeri (acil durum)
    return 5, COLORS['zone5'], HR_ZONES[5]['name']


# ================================================================
#  NAVİGASYON VE HESAPlAMALAR
#  ================================================================

def calculate_heading(points, idx):
    """
    Bisikletçinin hareket yönünü (heading) hesapla.
    
    Önceki ve sonraki point'ler arasındaki açı.
    
    Args:
        points (list): Tüm waypoint'ler
        idx (int): Mevcut waypoint index
    
    Returns:
        float: Yön açısı (derece, 0-360)
    """
    if idx <= 0 or idx >= len(points) - 1:
        return 0
    
    p1 = points[idx - 1]
    p2 = points[idx + 1]
    
    dlat = p2['lat'] - p1['lat']
    dlon = p2['lon'] - p1['lon']
    
    # atan2: dlon/dlat oranından açı hesapla
    angle = math.atan2(dlon, dlat)
    heading = math.degrees(angle)
    
    return heading


def calculate_power(speed_kmh, grade_percent, weight_kg=75, bike_kg=10):
    """
    Strava benzeri güç hesaplama (Watt).
    
    Fizik formülü:
    P = (F_gravity + F_rolling + F_aero) * velocity
    
    Args:
        speed_kmh (float): Hız (km/h)
        grade_percent (float): Eğim yüzdesi
        weight_kg (float): Bisikletçi ağırlığı (kg)
        bike_kg (float): Bisiklet ağırlığı (kg)
    
    Returns:
        float: Güç (Watt)
    """
    from config import POWER_CONFIG
    
    if speed_kmh <= 0:
        return 0
    
    # Hızı m/s'ye çevir
    speed_ms = speed_kmh / 3.6
    
    # Toplam ağırlık
    total_weight = weight_kg + bike_kg
    
    # Yerçekimi kuvveti (eğim)
    grade_rad = math.atan(grade_percent / 100)
    f_gravity = total_weight * 9.81 * math.sin(grade_rad)
    
    # Yuvarlanma direnci
    f_rolling = total_weight * 9.81 * math.cos(grade_rad) * POWER_CONFIG['crr']
    
    # Aerodinamik direnç
    # Rüzgar etkisi dahil
    effective_speed = speed_ms + POWER_CONFIG['wind_speed']
    f_aero = 0.5 * POWER_CONFIG['air_density'] * POWER_CONFIG['cda'] * (effective_speed ** 2)
    
    # Toplam kuvvet
    total_force = f_gravity + f_rolling + f_aero
    
    # Güç = Kuvvet × Hız
    power_wheel = total_force * speed_ms
    
    # Drivetrain kayıpları
    power_pedal = power_wheel / POWER_CONFIG['drivetrain_efficiency']
    
    return max(0, power_pedal)


# ================================================================
#  TEMEL VERİ KUESSENTİ
#  ================================================================

class DataHandler:
    """
    GPX verilerini yönet ve video frame'lerine göre interpolasyon yap.
    
    Temel görevler:
    - GPX dosyasını yükle
    - Video zamanı → GPX zamanına dönüştür
    - Verilleri interpolasyon yap (doğrusal)
    - Dinamik metrikler hesapla (hız, eğim, heading)
    """
    
    def __init__(self, gpx_file_path):
        """
        DataHandler'ı initialize et.
        
        Args:
            gpx_file_path (str): GPX dosyasının yolu
        """
        self.points = parse_gpx(gpx_file_path)
        
        if not self.points:
            raise ValueError("❌ GPX file is empty or invalid!")
        
        # GPX start time
        self.gpx_start = self.points[0]['t']
        
        # Total route distance
        self.total_route_m = self.points[-1]['cum_dist']
        
        # Power smoothing cache
        self.power_history = []
        
        print(f"📊 Data Summary:")
        print(f"   • Start: {self.gpx_start}")
        print(f"   • End: {self.points[-1]['t']}")
        print(f"   • Total Distance: {self.total_route_m/1000:.2f} km")
    
    def get_data(self, t_video):
        """
        Video zamanına göre tüm verileri interpolasyon yap.
        
        Args:
            t_video (float): Video zamanı (saniye)
        
        Returns:
            dict: İnterpolasyon yapılmış veri
                - lat, lon: Konum
                - ele: Yükseklik
                - hr: Kalp atış hızı
                - cad: Kadans
                - speed: Hız (km/h)
                - grade: Eğim (%)
                - cum_dist: Kümülatif mesafe
                - progress: Rota ilerlemesi (%)
                - idx: Mevcut waypoint index
                - heading: Hareket yönü (derece)
        """
        # GPX zamanını hesapla (offset ile)
        target_time = self.gpx_start + timedelta(seconds=t_video + ZAMAN_OFFSET_SANIYE)
        
        # Başlangıçtan önce
        if target_time <= self.points[0]['t']:
            data = dict(self.points[0])
            data.update({
                'speed': 0,
                'grade': 0,
                'power': 0,
                'progress': 0,
                'idx': 0,
                'heading': 0
            })
            return data
        
        # Bitiş sonrası
        if target_time >= self.points[-1]['t']:
            data = dict(self.points[-1])
            data.update({
                'speed': 0,
                'grade': 0,
                'power': 0,
                'progress': 100,
                'idx': len(self.points) - 1,
                'heading': 0
            })
            return data
        
        # İki point arasında interpolasyon yap
        for i in range(len(self.points) - 1):
            p1, p2 = self.points[i], self.points[i + 1]
            
            # Hedef zaman bu iki point arasında mı?
            if p1['t'] <= target_time <= p2['t']:
                # Zaman oranı hesapla (0-1)
                total_sec = (p2['t'] - p1['t']).total_seconds()
                if total_sec == 0:
                    continue
                
                ratio = (target_time - p1['t']).total_seconds() / total_sec
                
                # Konum linear interpolasyon
                lat = p1['lat'] + ratio * (p2['lat'] - p1['lat'])
                lon = p1['lon'] + ratio * (p2['lon'] - p1['lon'])
                ele = p1['ele'] + ratio * (p2['ele'] - p1['ele'])
                
                # Kalp atış interpolasyon
                hr = None
                if p1['hr'] and p2['hr']:
                    hr = int(p1['hr'] + ratio * (p2['hr'] - p1['hr']))
                elif p1['hr']:
                    hr = p1['hr']
                elif p2['hr']:
                    hr = p2['hr']
                
                # Kadans interpolasyon
                cad = None
                if p1['cad'] and p2['cad']:
                    cad = int(p1['cad'] + ratio * (p2['cad'] - p1['cad']))
                elif p1['cad']:
                    cad = p1['cad']
                elif p2['cad']:
                    cad = p2['cad']
                
                # Hız hesapla (m/s → km/h) using precomputed segment distance
                dist_seg = p2.get('seg_dist', None)
                if dist_seg is None:
                    # fallback to geodesic if seg_dist not present
                    dist_seg = geodesic((p1['lat'], p1['lon']), (p2['lat'], p2['lon'])).meters
                speed = (dist_seg / total_sec) * 3.6
                
                # Eğim hesapla (%)
                if dist_seg > 5:  # Minimum mesafe
                    grade = (p2['ele'] - p1['ele']) / dist_seg * 100
                else:
                    grade = 0
                
                # Kümülatif mesafe
                cur_dist = p1['cum_dist'] + dist_seg * ratio
                
                # İlerleme yüzdesi
                progress = (cur_dist / self.total_route_m) * 100 if self.total_route_m > 0 else 0
                
                # Hareket yönü
                heading = calculate_heading(self.points, i)
                
                # Güç hesapla ve smooth et
                raw_power = calculate_power(speed, grade)
                power = self._smooth_power(raw_power)
                
                return {
                    'lat': lat,
                    'lon': lon,
                    'ele': ele,
                    'hr': hr,
                    'cad': cad,
                    'speed': speed,
                    'grade': grade,
                    'power': power,
                    'cum_dist': cur_dist,
                    'progress': progress,
                    'idx': i,
                    'heading': heading
                }
        
        # Fallback (normal olmayacak)
        return {**self.points[0], 'speed': 0, 'grade': 0, 'power': 0, 'progress': 0, 'idx': 0, 'heading': 0}
    
    def get_elevation_range(self, idx, range_points):
        """
        Mevcut konumdan öncesindeki/sonrasındaki elevasyonu getir.
        
        Yükseklik profil grafiği için kullanılır.
        
        Args:
            idx (int): Merkez index
            range_points (int): Kaç point gösterilsin
        
        Returns:
            dict: min/max yükseklik ve point'ler
        """
        start_i = max(0, idx - range_points // 2)
        end_i = min(len(self.points), idx + range_points // 2)
        
        ele_values = [self.points[i]['ele'] for i in range(start_i, end_i)]
        
        return {
            'start_i': start_i,
            'end_i': end_i,
            'min': min(ele_values) if ele_values else 0,
            'max': max(ele_values) if ele_values else 0,
        }
    
    def _smooth_power(self, raw_power):
        """
        Güç değerini smooth et (moving average).
        
        Args:
            raw_power (float): Ham güç değeri
        
        Returns:
            float: Smooth edilmiş güç değeri
        """
        from config import POWER_CONFIG
        
        # Sınırları uygula
        clamped_power = max(POWER_CONFIG['min_power'], 
                           min(POWER_CONFIG['max_power'], raw_power))
        
        # History'ye ekle
        self.power_history.append(clamped_power)
        
        # Window boyutunu sınırla
        window_size = POWER_CONFIG['smoothing_window']
        if len(self.power_history) > window_size:
            self.power_history = self.power_history[-window_size:]
        
        # Moving average hesapla
        return sum(self.power_history) / len(self.power_history)


if __name__ == "__main__":
    print("✅ Data handler module loaded")
    print("   • parse_gpx(file)")
    print("   • get_hr_zone(hr)")
    print("   • DataHandler class")
