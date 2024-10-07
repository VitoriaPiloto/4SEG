import datetime

class Config:
    SECRET_KEY = '123'
    JWT_SECRET_KEY = '123'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)

    MAIL_SERVER = 'smtp.seuservidordeemail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'vitoriapiloto477@gmail.com'
    MAIL_PASSWORD = 'suasenha'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
