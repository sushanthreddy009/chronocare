# config.py
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/chronocare'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
