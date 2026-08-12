from flask import Flask

from config import Config
from extensions import db

from models import Employee
from routes import employee_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(employee_bp)


if __name__ == "__main__":
    app.run(debug=True)