FROM python:3.12

# Update system packages to fix vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Работна директория
WORKDIR /app


# Инсталиране на зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копиране на кода
COPY . .

# Expose порт
EXPOSE 8000

# Стартиране с autoreload
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]