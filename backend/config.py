class Config:
    SECRET_KEY = "dev-server"
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_PASSWORD_SALT = "some-random-salt"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    WTF_CSRF_ENABLED = False