FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y gcc build-essential pkg-config whois dnsutils && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 7112

CMD ["python", "main.py"]
