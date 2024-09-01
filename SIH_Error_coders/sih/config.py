import os

class Config:
    SECRET_KEY = os.getenv('311f671a9ec498740d7d27fd3b361ad3b4bd6705bb8cc705')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///example_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False