FROM python:3.10-bullseye

RUN apt-get update && apt-get install -y \
    libmagic-dev \
    poppler-utils \
    libreoffice \
    pandoc \
    tesseract-ocr

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

VOLUME ["/documents"]

CMD ["tail", "-f", "/dev/null"]
