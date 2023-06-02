class Config(object):
    MODEL = "gpt-3.5-turbo"
    OPENAI_API_KEY = "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"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass
