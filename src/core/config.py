from passlib.context import CryptContext
from starlette.config import Config, environ
from starlette.datastructures import CommaSeparatedStrings

config = Config(".env")

BASE_PATH_API = config('BASE_PATH_API')

SECRET_KEY = config('SECRET_KEY', default='secretkey')
ALGORITHM = "HS256"
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings, default=['*'])

DEBUG = config('DEBUG', cast=bool, default=False)

ACCESS_TOKEN_EXPIRES = config('ACCESS_TOKEN_EXPIRES', default=24 * 7)
MONGODB_NAME = config("MONGODB_NAME")
MONGODB_URI = config("MONGODB_URI")

database_name = MONGODB_NAME
if environ.get('TESTING') == 'TRUE':
    database_name = f'test-{database_name}'
