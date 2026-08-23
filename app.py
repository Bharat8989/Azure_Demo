from flask import Flask

from config.db_config import Config
from extensions import db

from controllers.student_controller import student_controller
from controllers.teacher_controller import teacher_controller



app = Flask(__name__)


# Database configuration
app.config.from_object(Config)


# Initialize SQLAlchemy
db.init_app(app)


# Register Blueprints
app.register_blueprint(student_controller)
app.register_blueprint(teacher_controller)


# Create tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":

    print("\n" + "=" * 50)
    print(" ACTIVE ROUTES IN YOUR FLASK APP ".center(50, "*"))
    print("=" * 50)

    for rule in app.url_map.iter_rules():

        if rule.endpoint != "static":
            methods = ", ".join(
                rule.methods - {"OPTIONS", "HEAD"}
            )

            print(
                f"Route: {str(rule):<30} | "
                f"Methods: [{methods}]"
            )

    print("=" * 50 + "\n")

    app.run(debug=True)