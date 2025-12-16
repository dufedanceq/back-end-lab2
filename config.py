import os

SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL', 
    'postgresql://user:password@localhost:5432/expenses'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

API_TITLE = "Expense Tracker API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"