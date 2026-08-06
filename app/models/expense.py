from app.extensions import db
from app.constants import HIGH_EXPENSE_LIMIT

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
    expense_date = db.Column(
        db.Date,
        nullable=False,
        default=db.func.current_date()
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    

    @property
    def status(self):
        return "High" if self.amount > HIGH_EXPENSE_LIMIT else "Normal"

    @property
    def status_class(self):
        return "bg-danger" if self.amount > HIGH_EXPENSE_LIMIT else "bg-success"

    def __repr__(self):
        return f"<Expense {self.title}>"