from flask import Blueprint, jsonify, request

from services.student_service import StudentService


student_controller = Blueprint(
    "student_controller",
    __name__,
    url_prefix="/student"
)





# =========================
# GET ALL STUDENTS
# =========================
@student_controller.route("/", methods=["GET"])
def get_students():

    students = StudentService.get_all_students()

    return jsonify([
        {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "marks": student.marks
        }
        for student in students
    ])


# =========================
# CREATE STUDENT
# =========================
@student_controller.route("/", methods=["POST"])
def save_student():

    data = request.get_json()

    student = StudentService.create_student(data)

    return jsonify({
        "message": "Student saved successfully",
        "id": student.id
    }), 201


# =========================
# UPDATE STUDENT
# =========================
@student_controller.route("/<int:id>", methods=["PUT"])
def update_student(id):

    data = request.get_json()

    student = StudentService.update_student(
        id,
        data
    )

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify({
        "message": "Student updated successfully",
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "marks": student.marks
    }), 200


# =========================
# DELETE STUDENT
# =========================
@student_controller.route("/<int:id>", methods=["DELETE"])
def delete_student(id):

    student = StudentService.delete_student(id)

    if student is None:
        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify({
        "message": "Student deleted successfully",
        "id": id
    }), 200