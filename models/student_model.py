from extensions import db


class Student(db.Model):

    __tablename__ = "student"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True
    )

    marks = db.Column(
        db.Integer
    )