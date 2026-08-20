from flask import Blueprint, jsonify, request
from services.teacher_service import TeacherService

teacher_controller = Blueprint(
    "teacher_controller",
    __name__
)

@teacher_controller.route("/teachers", methods=["GET"])
def get_teachers():
    teachers = TeacherService.get_all_teachers()
    return jsonify([
        {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "subject": teacher.subject
        }
        for teacher in teachers
    ])

@teacher_controller.route("/teacher", methods=["POST"])
def save_teacher():
    data = request.get_json()
    teacher = TeacherService.create_teacher(data)
    return jsonify({
        "message": "Teacher saved successfully",
        "id": teacher.id
    }), 201
    

@teacher_controller.route("/teacher/<int:id>", methods=["PUT"])
def update_teacher(id):
    data = request.get_json()
    teacher = TeacherService.update_teacher(id, data)
    
    if teacher is None:
        return jsonify({"message": "Teacher not found"}), 404

    return jsonify({
        "message": "Teacher updated successfully",
        "id": teacher.id,
        "name": teacher.name,
        "email": teacher.email,
        "subject": teacher.subject
    })

@teacher_controller.route("/teacher/<int:id>", methods=["DELETE"])
def delete_teacher(id):
    teacher = TeacherService.delete_teacher(id)
    
    if teacher is None:
        return jsonify({"message": "Teacher not found"}), 404

    return jsonify({
        "message": "Teacher deleted successfully",
        "id": id
    })
