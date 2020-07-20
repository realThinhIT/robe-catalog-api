from .base import _Config


class _DevConfig(_Config):
    SQL_ALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://gotit:123456@localhost/catalog_api'
    DEBUG = True


config = _DevConfig
