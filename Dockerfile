# Используйте официальный образ Python как родительский образ
FROM python:3.10-slim

# Установка distutils
RUN apt-get update && apt-get install -y python3-distutils

# Установите рабочую директорию в контейнере
WORKDIR /app

# Скопируйте файл requirements.txt в контейнер
COPY requirements.txt ./

# Установите любые необходимые пакеты указанные в requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте содержимое локальной директории src в рабочую директорию контейнера
COPY src/ ./

# Сделайте порт доступным для мира вне контейнера
EXPOSE 5000

# Определите переменную среды
ENV NAME World

# Запустите приложение при запуске контейнера
CMD ["python", "app.py"]
