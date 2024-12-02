import os
from dotenv import load_dotenv

load_dotenv()

LANGUAGES = ["en", "fr"]

SECRET_KEY = os.environ.get('SECRET_KEY')

database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://')

SQLALCHEMY_DATABASE_URI = database_url

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
