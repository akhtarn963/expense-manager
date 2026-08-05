from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    session, 
    g,
    flash
    )
from app.models import Expense, db, Category
from app.utils import calculate_statistics
from app.decorators import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import constants

expense_bp = Blueprint("expense", __name__)

@expense_bp.route("/expenses")
@login_required
def home():  
    expenses = Expense.query.filter_by(user_id=g.user.id).all()
    stats = calculate_statistics(expenses)
    
    return render_template(
        "expenses/index.html",
        expenses=expenses,
        stats=stats
    )

@expense_bp.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense():

    categories = db.session.query(Category).all()
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        if not category_id:
            flash("Please select a category.", constants.FLASH_DANGER)
            return redirect(url_for("expense.add_expense"))
        expense = Expense(
            title = request.form['title'],
            amount = request.form['amount'],
            user_id=g.user.id,
            category_id=request.form['category_id']
        )
        db.session.add(expense)
        db.session.commit()
        flash("Expense added successfully.", constants.FLASH_SUCCESS)
        return redirect(url_for("expense.home"))
    return render_template("expenses/add.html", categories=categories)

@expense_bp.route('/edit-expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=g.user.id
    ).first_or_404()
    categories = db.session.query(Category).all()
    if request.method == 'POST':
        expense.title = request.form["title"]
        expense.amount = request.form["amount"]
        expense.category_id = request.form["category_id"]
        db.session.commit()
        flash("Expense updated successfully.", constants.FLASH_SUCCESS)
        return redirect(url_for("expense.home"))

    return render_template("expenses/edit.html", expense=expense, categories=categories)

@expense_bp.route('/delete-expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    
    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=g.user.id
    ).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully.", constants.FLASH_SUCCESS)
    return redirect(url_for("expense.home"))

