# Temel olarak Python 3.12 içeren bir Linux dağıtımı kullanın
FROM python:3.12-slim

# Uygulamanın çalışacağı dizini belirleyin
WORKDIR /app

# OpenCV'nin GUI bağımlılıklarını (Qt) sistem düzeyinde kurun
# Bu, "libQt5Widgets" hatasını çözer.
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libavif-dev \
    libqt5gui5 \
    libqt5widgets5 \
    libqt5core5a \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libavcodec-extra \
    libx264-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    && rm -rf /var/lib/apt/lists/*


# Bağımlılıkları requirements.txt üzerinden yükleyin (varsa)
# Klasörde requirements.txt yoksa, varsayılan paketleri yedek olarak yükleriz.
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt \
    || pip install --no-cache-dir opencv-python gpxpy numpy moviepy geopy tqdm

# Not: Bu repo doğrudan çalışma dizinini podman ile bağladığınız için
# uygulama dosyalarını build sırasında kopyalamaya gerek yok. Çalıştırmak için:
#   podman build -t video-proje:latest .
#   podman run --rm -v "$(pwd):/app:rw,z" --userns=keep-id video-proje python3 video_renderer.py

