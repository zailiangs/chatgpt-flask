class Config(object):
    MODEL = "gpt-3.5-turbo"
    OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass
