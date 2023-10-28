#!/bin/bash

# Ruta a la carpeta de tu proyecto py_chain
PROJECT_DIR="C:\Users\Emilio\Desktop\Smart_Contracts_Course\BlockchainCert\py_chain"

# Solicita al usuario el número de puerto
read -p "Por favor, ingresa el número de puerto en el que deseas lanzar el servidor web de Django: " PORT

# Navega al directorio del proyecto Django
cd "$PROJECT_DIR"

# Ejecuta el servidor web de Django en el puerto especificado
python manage.py runserver $PORT

# Desactiva el entorno virtual cuando hayas terminado
deactivate
