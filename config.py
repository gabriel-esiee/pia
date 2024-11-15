class Config(object):
    DEBUG = True
    LANGUAGES = ['en', 'fr']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite'
    SECRET_KEY = 'ckyre'