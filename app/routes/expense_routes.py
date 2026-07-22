from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Expense, db
from app.utils import calculate_statistics

expense_bp = Blueprint("expense", __name__)

@expense_bp.route("/")
def home():  
    expenses = Expense.query.all()
    stats = calculate_statistics(expenses)
    
    return render_template(
        "home.html",
        expenses=expenses,
        stats=stats
    )

@expense_bp.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':

        expense = Expense(
            title = request.form['title'],
            amount = request.form['amount']
        )
        db.session.add(expense)
        db.session.commit()
        
        return redirect(url_for("expense.home"))
    return render_template("add_expense.html")

@expense_bp.route('/edit-expense/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):

    expense = db.get_or_404(Expense, expense_id)
    if request.method == 'POST':
        expense.title = request.form["title"]
        expense.amount = request.form["amount"]
        db.session.commit()
        return redirect(url_for("expense.home"))

    return render_template("edit_expense.html", expense=expense)

@expense_bp.route('/delete-expense/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    
    expense = db.get_or_404(Expense, expense_id)
    db.session.delete(expense)
    db.session.commit()

    return redirect(url_for("expense.home"))