from flask import Flask

from config.db_config import Config
from extensions import db

from controllers.student_controller import student_controller


app = Flask(__name__)


# Database configuration
app.config.from_object(Config)


# Initialize SQLAlchemy
db.init_app(app)


# Register Blueprint
app.register_blueprint(student_controller)


# Create tables
with app.app_context():

    db.create_all()


if __name__ == "__main__":

    app.run(debug=True)