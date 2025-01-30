import os

class Config:
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
