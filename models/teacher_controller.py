from extensions import db


class Teacher(db.Model):

    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), nullable=False, unique=True)

    subject = db.Column(db.String(100), nullable=False)

    experience = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "experience": self.experience
        }