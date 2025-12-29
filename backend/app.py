from flask import Flask
from config import Config
from models import db
def current_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app=app)

    with app.app_context():
        import routes
        db.create_all()
    return app

if __name__ == "__main__":
    app = current_app()
    app.run()