import json
import logging
import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    @classmethod
    def init_app(cls, app):
        """Send logs to stdout."""
        file_handler = logging.StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True


class UnitTestingConfig(Config):
    TESTING = True
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True


class IntegrationTestingConfig(Config):
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    if os.getenv("VCAP_SERVICES"):
        services = json.loads(os.getenv("VCAP_SERVICES"))
        redis_env = services["p-redis"][0]["credentials"]
        REDIS_URL = "redis://" + redis_env["password"] + "@" + redis_env["host"] + ":" + redis_env["port"]


config = {
    "development": DevelopmentConfig,
    "unit_testing": UnitTestingConfig,
    "integration_testing": IntegrationTestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
