from app.extensions import db

HIGH_EXPENSE_LIMIT = 3000

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    @property
    def status(self):
        return "High" if self.amount > HIGH_EXPENSE_LIMIT else "Normal"

    @property
    def status_class(self):
        return "bg-danger" if self.amount > HIGH_EXPENSE_LIMIT else "bg-success"

    def __repr__(self):
        return f"<Expense {self.title}>"