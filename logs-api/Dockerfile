FROM python:3.11-slim

# Crear carpeta de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#ENV RABBITMQ_USER=guest
#ENV RABBITMQ_PASSWORD=guest
#ENV RABBITMQ_HOST=rabbitmq
#ENV PUBLIC_KEY_PATH=/app/public_key.pem
# Copiar TODO el código de la aplicación, incluyendo la carpeta broker/
COPY . .

# Exponer puerto
EXPOSE 6000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6000"]
