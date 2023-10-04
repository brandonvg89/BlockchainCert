#!/bin/bash

# Ruta a la carpeta de tu proyecto py_chain
PROJECT_DIR="/c/Users/delao/Documents/BlockchainPRJ/py_chain"

# Nombre del entorno virtual
VIRTUAL_ENV_NAME="blockchain_env"

# Activa el entorno virtual
source "/c/Users/delao/Documents/BlockchainPRJ/blockchain_env/Scripts/activate"

# Solicita al usuario el número de puerto
read -p "Por favor, ingresa el número de puerto en el que deseas lanzar el servidor web de Django: " PORT

# Navega al directorio del proyecto Django
cd "$PROJECT_DIR"

# Ejecuta el servidor web de Django en el puerto especificado
python manage.py runserver $PORT

# Desactiva el entorno virtual cuando hayas terminado
deactivate
