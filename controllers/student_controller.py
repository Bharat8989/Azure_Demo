from flask import Blueprint, jsonify, request

from services.student_service import StudentService


student_controller = Blueprint(
    "student_controller",
    __name__
)


@student_controller.route(
    "/students",
    methods=["GET"]
)
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


@student_controller.route(
    "/student",
    methods=["POST"]
)
def save_student():

   
    data = request.get_json()

    
    student = StudentService.create_student(data)

    return jsonify({
        "message": "Student saved successfully",
        "id": student.id
    }), 201


@student_controller.route(
    "/student/<int:id>",
    methods=["PUT"]
)
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
    })


@student_controller.route(
    "/student/<int:id>",
    methods=["DELETE"]
)
def delete_student(id):

    student = StudentService.delete_student(id)

    if student is None:

        return jsonify({
            "message": "Student not found"
        }), 404

    return jsonify({
        "message": "Student deleted successfully",
        "id": id
    })
