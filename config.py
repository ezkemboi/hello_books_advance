class Config(object):
    """
    All common configurations for app goes here.
    """


class DevelopmentConfig(Config):
    """
    Only development configurations goes here.
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Only production configurations goes here.
    """
    DEBUG = False

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}