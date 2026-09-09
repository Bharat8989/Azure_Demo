from functools import wraps

from flask import Blueprint, jsonify, request

from schemas.student_schema import (
    validate_forget_password_payload,
    validate_login_payload,
    validate_register_payload,
)


student_bp = Blueprint(
    "student",
    __name__
)


def get_json_body():
    if not request.is_json:
        return None

    return request.get_json(silent=True)


def protected_route(service):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            authorization = request.headers.get("Authorization", "")

            if not authorization.startswith("Bearer "):
                return jsonify({
                    "success": False,
                    "message": "Authentication token is required."
                }), 401

            token = authorization[7:].strip()

            if not token:
                return jsonify({
                    "success": False,
                    "message": "Authentication token is required."
                }), 401

            student = service.verify_token(token)

            if not student:
                return jsonify({
                    "success": False,
                    "message": "Invalid or expired authentication token."
                }), 401

            return function(student, *args, **kwargs)

        return wrapper

    return decorator


def register_routes(service):

    @student_bp.post("/register")
    def register():
        data = get_json_body()

        errors = validate_register_payload(data)

        if errors:
            return jsonify({
                "success": False,
                "message": "Validation failed.",
                "errors": errors
            }), 400

        try:
            student = service.register(
                name=data["name"],
                email=data["email"],
                password=data["password"]
            )

            return jsonify({
                "success": True,
                "message": "Registration successful.",
                "student": student.to_dict()
            }), 201

        except ValueError as exc:
            return jsonify({
                "success": False,
                "message": str(exc)
            }), 400

    @student_bp.post("/login")
    def login():
        data = get_json_body()

        errors = validate_login_payload(data)

        if errors:
            return jsonify({
                "success": False,
                "message": "Validation failed.",
                "errors": errors
            }), 400

        result = service.login(
            email=data["email"],
            password=data["password"]
        )

        if not result:
            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "token": result["token"],
            "student": result["student"]
        }), 200

    @student_bp.post("/forget-password")
    def forget_password():
        data = get_json_body()

        errors = validate_forget_password_payload(data)

        if errors:
            return jsonify({
                "success": False,
                "message": "Validation failed.",
                "errors": errors
            }), 400

        service.request_password_reset(
            email=data["email"]
        )

        # Deliberately generic to prevent account enumeration.
        return jsonify({
            "success": True,
            "message": (
                "If an account exists for that email, "
                "password reset instructions have been generated."
            )
        }), 200

    @student_bp.get("/dashboard")
    @protected_route(service)
    def dashboard(student):
        return jsonify({
            "success": True,
            "message": "Dashboard data loaded successfully.",
            "student": student.to_dict()
        }), 200

    return student_bp