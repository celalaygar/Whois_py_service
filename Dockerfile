FROM python:3.12-slim

# Sistem güncelle ve gerekli araçları kur
RUN apt-get update && \
    apt-get install -y gcc build-essential pkg-config whois dnsutils && \
    rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Gereksinim dosyasını kopyala ve yükle
COPY requirements.txt .

# Pip'i güncelle ve gereksinimleri yükle
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Uygulamayı kopyala
COPY . .

# Ortam değişkenleri
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Flask portu
EXPOSE 7112

# Başlat
CMD ["python", "main.py"]
