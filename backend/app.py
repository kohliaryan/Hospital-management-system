from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from config import Config
from models import db, User, Role
from create_initial_data import create_initial_data

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    with app.app_context():
        import routes
        db.create_all()
        create_initial_data()  

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
