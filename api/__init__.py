import os
from flask import Flask

app = Flask(__name__)


class DatabaseConfig:
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "app")
    password = os.getenv("DB_PASSWORD", "pass")


from api import routes
