FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 10000

# Запуск фиктивного HTTP-сервера и бота
CMD python -m http.server 8000 & python bot.py
