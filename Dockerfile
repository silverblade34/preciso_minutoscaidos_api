# Usamos una imagen base de Python
FROM python:3.8-alpine

# Establecemos el directorio de trabajo en /app
WORKDIR /app

# Copiamos los archivos necesarios para la aplicación a /app
COPY . .

# Instalamos las dependencias de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Establecemos la variable de entorno para Flask
ENV FLASK_APP=app.py

# Exponemos el puerto 8000 para que pueda ser accedido desde fuera del contenedor
EXPOSE 3222
# Ejecutamos Gunicorn para servir la aplicación en el puerto 8000
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:3222", "app:app"]

# FROM python:3.8.10

# WORKDIR /app
# # Instalamos python dentro del contenedor de nuestra app
# COPY requirements.txt requirements.txt

# RUN pip3 install -r requirements.txt

# COPY . .

# # Generamos las dependencias
# # Va a instalar dentro del contenedor va a instalar todos los modulos que la app necesita

# CMD ["python3","app.py"]
