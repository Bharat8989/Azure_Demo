from extensions import db
from models.student_model import Student


class StudentRepository:

    @staticmethod
    def get_all_students():

        return Student.query.all()

    @staticmethod
    def get_student_by_id(student_id):

        return db.session.get(Student, student_id)

    @staticmethod
    def save_student(student):

        db.session.add(student)
        db.session.commit()

        return student

    @staticmethod
    def update_student():

        db.session.commit()

    @staticmethod
    def delete_student(student):

        db.session.delete(student)
        db.session.commit()