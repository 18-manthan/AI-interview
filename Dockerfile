# syntax=docker/dockerfile:1
FROM python:3.10.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y portaudio19-dev&& apt-get install -y \
    libgl1-mesa-glx && pip install opencv-python
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
CMD ["daphne", "projectname.asgi:application", "--port", "8000"]
