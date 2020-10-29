import os

from flask import Flask
from flask_cors import CORS

from config import DevelopmentConfig, ProductionConfig
from src.application.api import api

app = Flask(__name__)

if os.environ["FLASK_APP_ENV"] == "dev":
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)

CORS(
    app,
    origins=app.config["ORIGINS"],
    expose_headers=["Access-Control-Allow-Origin"],
    supports_credentials=True,
)

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
