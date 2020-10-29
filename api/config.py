import os


def get_configuration():
    if os.environ["FLASK_APP_ENV"] == "dev":
        return DevelopmentConfig
    else:
        return ProductionConfig


class DevelopmentConfig(object):
    """Base config, uses staging database server."""

    ENV = "development"
    DEBUG = True
    POSTGRESQL_SETTINGS = {
        "host" : "postgres",
        "database" : "spotify",
        "user" : "postgres",
        "password" : "postgres",
        "port" : 5432,
    }
    ORIGINS = ["http://localhost:5000"]

class ProductionConfig(object):
    ENV = "production"
    DEBUG = False
    POSTGRESQL_SETTINGS = {
        "host" : "postgresql",
        "database" : "spotify",
        "user" : "postgres",
        "password" : "postgres",
        "port" : 5432,
    }
    ORIGINS = ["http://localhost:5000"]
