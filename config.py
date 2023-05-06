class Config(object):
    MODEL = "gpt-3.5-turbo"
    OPENAI_API_KEY = "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"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass
