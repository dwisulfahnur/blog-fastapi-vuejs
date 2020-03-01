from starlette.config import Config
from starlette.datastructures import Secret, CommaSeparatedStrings

config = Config(".env")

SECRET_KEY = config('SECRET_KEY', cast=Secret)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)

DEBUG = config('DEBUG', cast=bool, default=False)

MONGODB_NAME = config("MONGODB_NAME")
MONGODB_URI = config("MONGODB_URI")

database_name = MONGODB_NAME
