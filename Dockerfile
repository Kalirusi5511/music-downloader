# Verwenden Sie ein leichtgewichtiges Python-Image als Basis
FROM python:3.11-slim

# Installieren Sie ffmpeg (Schlüsselabhängigkeit für yt-dlp)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Legen Sie das Arbeitsverzeichnis fest
WORKDIR /app

# Kopieren Sie zuerst die Abhängigkeitsdatei und installieren Sie Python-Pakete (nutzen Sie den Docker-Cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den restlichen Projektcode
COPY . .

# Starten Sie die Anwendung mit Gunicorn (passen Sie es an den Namen in Ihrer app.py an)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
