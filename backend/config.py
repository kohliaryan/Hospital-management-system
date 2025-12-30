class Config:
    SECRET_KEY = "dev-server"

    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🔑 Flask-Security REQUIRED settings
    SECURITY_PASSWORD_SALT = "super-secret-salt"
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SINGLE_HASH = True

    # Flask-Security options
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    # Disable CSRF for development
    WTF_CSRF_ENABLED = False
