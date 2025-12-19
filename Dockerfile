# syntax=docker/dockerfile:1
FROM python:3.10.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libgl1-mesa-glx \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install opencv-python

WORKDIR /code
COPY requirements.txt /code/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir dlib==19.24.0

RUN pip install -r requirements.txt

COPY . /code/
CMD ["daphne", "projectname.asgi:application", "--port", "8000"]