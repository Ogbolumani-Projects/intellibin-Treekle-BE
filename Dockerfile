FROM python:3.12-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev python3-dev build-essential

# Install dependencies only if requirements.txt is present in the mounted volume
COPY requirements.txt /app/  
RUN pip install --no-cache-dir -r /app/requirements.txt