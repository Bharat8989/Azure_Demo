from extensions import db
from models.teacher_model import Teacher


class TeacherRepository:

    @staticmethod
    def get_all_teachers():

        return Teacher.query.all()

    @staticmethod
    def get_teacher_by_id(teacher_id):

        return db.session.get(
            Teacher,
            teacher_id
        )

    @staticmethod
    def save_teacher(teacher):

        db.session.add(teacher)
        db.session.commit()

        return teacher

    @staticmethod
    def update_teacher():

        db.session.commit()

    @staticmethod
    def delete_teacher(teacher):

        db.session.delete(teacher)
        db.session.commit()
