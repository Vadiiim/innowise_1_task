FROM python:3.9

WORKDIR /app

ADD . /app
COPY . /app

RUN pip install -r requirements.txt

# Установите netcat-openbsd
RUN apt-get update && apt-get install -y netcat-openbsd

COPY wait-for-it.sh /app/wait-for-it.sh

RUN chmod +x /app/wait-for-it.sh

EXPOSE 8000

CMD ["python", "main.py"]
