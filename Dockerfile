# Используйте официальный образ Python как родительский образ
FROM python:3.10-slim

# Установка distutils
RUN apt-get update && apt-get install -y python3-distutils

# Создайте рабочую директорию в контейнере
WORKDIR /app

# Скопируйте все содержимое корневой директории проекта в контейнер
COPY . /app

# Скопируйте файл requirements.txt в контейнер
COPY requirements.txt ./

# Установите любые необходимые пакеты указанные в requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Добавьте /app/src в PYTHONPATH
ENV PYTHONPATH=/app/src

# Сделайте порт доступным для мира вне контейнера
EXPOSE 5000

# Определите переменную среды
ENV NAME World

# Запустите приложение при запуске контейнера
CMD ["python", "src/online_store/app.py"]
