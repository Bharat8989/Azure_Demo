from extensions import db


class Teacher(db.Model):

    __tablename__ = "teacher"

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

    subject = db.Column(
        db.String(100)
    )