from app.extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

    expenses = db.relationship(
        "Expense",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"