import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv('APP_ENV', '*******')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', '*******')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '*******')
DATABASE_HOST = os.getenv('DATABASE_HOST', '*******')
DATABASE_PORT = os.getenv('DATABASE_PORT', '*******')
DATABASE_NAME = os.getenv('DATABASE_NAME', '*******')


MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_FROM = os.getenv('MAIL_FROM')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')
