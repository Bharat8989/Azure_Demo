from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.student import Student


class StudentRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, student: Student) -> Student:
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)

        return student

    def get_by_id(
        self,
        student_id: str
    ) -> Optional[Student]:

        statement = select(Student).where(
            Student.student_id == student_id
        )

        return self.session.scalar(statement)

    def get_by_email(
        self,
        email: str
    ) -> Optional[Student]:

        statement = select(Student).where(
            Student.email == email.lower()
        )

        return self.session.scalar(statement)

    def exists_by_email(
        self,
        email: str
    ) -> bool:

        statement = select(Student.student_id).where(
            Student.email == email.lower()
        )

        return self.session.scalar(statement) is not None

    def update(self, student: Student) -> Student:
        self.session.commit()
        self.session.refresh(student)

        return student