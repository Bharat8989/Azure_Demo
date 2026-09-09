from flask import Flask, jsonify
from flask_cors import CORS

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.config import Config
from models.student import Base
from repositories.student_repo import StudentRepository
from services.student_service import StudentService
from controllers.student_ctrl import register_routes


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # ---------------------------------------------------------
    # MySQL Engine
    # ---------------------------------------------------------

    engine = create_engine(
        Config.DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=280,
        echo=False
    )

    # ---------------------------------------------------------
    # Create database tables
    # ---------------------------------------------------------

    Base.metadata.create_all(
        bind=engine
    )

    # ---------------------------------------------------------
    # CORS
    # ---------------------------------------------------------

    CORS(
        app,
        resources={
            r"/*": {
                "origins": app.config[
                    "FRONTEND_ORIGINS"
                ],
                "methods": [
                    "GET",
                    "POST",
                    "OPTIONS"
                ],
                "allow_headers": [
                    "Content-Type",
                    "Authorization"
                ]
            }
        }
    )

    # ---------------------------------------------------------
    # Database session
    # ---------------------------------------------------------

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )

    # One session for this application instance.
    db_session = SessionLocal()

    # ---------------------------------------------------------
    # Repository
    # ---------------------------------------------------------

    repository = StudentRepository(
        db_session
    )

    # ---------------------------------------------------------
    # Service
    # ---------------------------------------------------------

    service = StudentService(
        repository
    )

    # ---------------------------------------------------------
    # Routes
    # ---------------------------------------------------------

    student_blueprint = register_routes(
        service
    )

    app.register_blueprint(
        student_blueprint
    )

    # ---------------------------------------------------------
    # Error handlers
    # ---------------------------------------------------------

    @app.errorhandler(404)
    def not_found(_error):

        return jsonify({
            "success": False,
            "message": "Endpoint not found."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):

        return jsonify({
            "success": False,
            "message": "HTTP method is not allowed."
        }), 400

    @app.errorhandler(413)
    def request_too_large(_error):

        return jsonify({
            "success": False,
            "message": "Request payload is too large."
        }), 400

    @app.errorhandler(500)
    def internal_server_error(_error):

        return jsonify({
            "success": False,
            "message": "Internal server error."
        }), 500

    # ---------------------------------------------------------
    # Health check
    # ---------------------------------------------------------

    @app.get("/health")
    def health():

        return jsonify({
            "success": True,
            "message": "Student Portal API is running."
        }), 200

    return app


app = create_app()


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )