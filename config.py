import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement depuis le fichier .env

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une_cle_secrete'
    MYSQL_DATABASE_HOST = os.environ.get('HOST')
    MYSQL_DATABASE_PORT = os.environ.get('PORT')
    MYSQL_DATABASE_USER = os.environ.get('USER')
    MYSQL_DATABASE_PASSWORD = os.environ.get('PASSWORD')
    MYSQL_DATABASE_DB = os.environ.get('DATABASE')
