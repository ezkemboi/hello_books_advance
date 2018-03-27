class Config(object):
    """
    All common configurations for app goes here.
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = 'iusertsisss'


class DevelopmentConfig(Config):
    """
    Only development configurations goes here.
    """
    DEBUG = True


class TestingConfig(Config):
    """
    Configuration for testing goes here.
    """
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """
    Only production configurations goes here.
    """
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
