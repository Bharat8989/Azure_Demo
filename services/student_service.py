from models.student_model import Student
from repositories.student_repository import StudentRepository


class StudentService:

    @staticmethod
    def get_all_students():

        students = StudentRepository.get_all_students()

        return students

    @staticmethod
    def create_student(data: dict):

        student = Student(
            name=data.get("name"),
            email=data.get("email"),
            marks=data.get("marks")
        )

        return StudentRepository.save_student(student)
    @staticmethod
    def update_student(student_id, data):

        student = StudentRepository.get_student_by_id(student_id)

        if student is None:
            return None

        student.name = data.get(
            "name",
            student.name
        )

        student.email = data.get(
            "email",
            student.email
        )

        student.marks = data.get(
            "marks",
            student.marks
        )

        StudentRepository.update_student()

        return student

    @staticmethod
    def delete_student(student_id):

        student = StudentRepository.get_student_by_id(student_id)

        if student is None:
            return None

        StudentRepository.delete_student(student)

        return student
