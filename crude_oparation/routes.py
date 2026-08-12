from flask import Blueprint, request, jsonify
from extensions import db
from models import Employee

employee_bp = Blueprint("employee", __name__)

@employee_bp.route("/employees", methods=["POST"])
def create_employee():

    data = request.get_json()
    
    # Check if employee with this name already exists
    existing_employee = Employee.query.filter_by(name=data["name"]).first()
    if existing_employee is not None:
        return jsonify({
            "message": "Employee with this name already exists"
        }), 400

    employee = Employee(
        name=data["name"],
        email=data["email"],
        salary=data["salary"]
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee created successfully",
        "id": employee.id,
        "name":employee.name,
        "salary":employee.salary
    }), 201

@employee_bp.route("/employees", methods=["GET"])
def get_employees():

    employees = Employee.query.all()

    result = []

    for employee in employees:
        result.append({
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "salary": employee.salary
        })

    return jsonify(result)

@employee_bp.route("/employees/<int:id>", methods=["PUT"])
def update_employee(id):

    employee = Employee.query.get(id)

    if employee is None:
        return jsonify({
            "message": "Employee not found"
        }), 404

    data = request.get_json()

    employee.name = data["name"]
    employee.email = data["email"]
    employee.salary = data["salary"]

    db.session.commit()

    return jsonify({
        "message": "Employee updated successfully"
    })

@employee_bp.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):

    employee = Employee.query.get(id)

    if employee is None:
        return jsonify({
            "message": "Employee not found"
        }), 404

    db.session.delete(employee)
    db.session.commit()

    return jsonify({
        "message": "Employee deleted successfully"
    })