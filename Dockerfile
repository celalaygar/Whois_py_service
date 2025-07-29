FROM python:3.11-slim

# Sistem güncelle ve derleme araçlarını kur
RUN apt-get update && \
    apt-get install -y gcc build-essential pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Gereksinim dosyasını kopyala ve yükle
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı kopyala
COPY . .

# Ortam değişkenlerini kullanmak için (isteğe bağlı)
ENV FLASK_ENV=production

# Flask varsayılan portu
EXPOSE 7102

# Başlat
CMD ["python", "Main.py"]
