from models.teacher_model import Teacher
from repositories.teacher_repository import TeacherRepository


class TeacherService:

    @staticmethod
    def get_all_teachers():

        teachers = TeacherRepository.get_all_teachers()

        return teachers

    @staticmethod
    def create_teacher(data: dict):

        teacher = Teacher(
            name=data.get("name"),
            email=data.get("email"),
            subject=data.get("subject")
        )

        return TeacherRepository.save_teacher(teacher)

    @staticmethod
    def update_teacher(teacher_id, data):

        teacher = TeacherRepository.get_teacher_by_id(
            teacher_id
        )

        if teacher is None:
            return None

        teacher.name = data.get(
            "name",
            teacher.name
        )

        teacher.email = data.get(
            "email",
            teacher.email
        )

        teacher.subject = data.get(
            "subject",
            teacher.subject
        )

        TeacherRepository.update_teacher()

        return teacher

    @staticmethod
    def delete_teacher(teacher_id):

        teacher = TeacherRepository.get_teacher_by_id(
            teacher_id
        )

        if teacher is None:
            return None

        TeacherRepository.delete_teacher(teacher)

        return teacher