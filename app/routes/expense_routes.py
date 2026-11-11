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
from datetime import datetime
from sqlalchemy import func

expense_bp = Blueprint("expense", __name__)

@expense_bp.route("/expenses")
@login_required
def home():  
    search = request.args.get("search","").strip()
    category_id = request.args.get("category_id","")
    date_from = request.args.get("date_from", "").strip()
    date_to = request.args.get("date_to", "").strip()

    try:
        start_date = (
            datetime.strptime(date_from, "%Y-%m-%d").date()
            if date_from else None
        )

        end_date = (
            datetime.strptime(date_to, "%Y-%m-%d").date()
            if date_to else None
        )

        if start_date and end_date and start_date > end_date:
            raise ValueError

    except ValueError:
        flash(
            "Please enter valid dates. From Date cannot be after To Date.",
            constants.FLASH_DANGER
        )
        return redirect(url_for("expense.home"))


    min_amount = request.args.get("min_amount", "").strip()
    max_amount = request.args.get("max_amount", "").strip()   
    try: 
        min_value = float(min_amount) if min_amount else None
        max_value = float(max_amount) if max_amount else None

        if min_value is not None and min_value < 0:
            raise ValueError

        if max_value is not None and max_value < 0:
            raise ValueError

        if min_value is not None and max_value is not None:
            if min_value > max_value:
                raise ValueError

    except ValueError:
        flash(
            "Please enter valid amounts. Minimum cannot exceed maximum.",
            constants.FLASH_DANGER
        )
        return redirect(url_for("expense.home"))

    page = request.args.get("page", 1, type=int)


    expenses = Expense.query.filter_by(user_id=g.user.id).all()
    stats = calculate_statistics(expenses)

    query = Expense.query.filter_by(user_id=g.user.id)
    if search:
        query = query.filter(Expense.title.ilike(f"%{search}%"))
    if category_id:
        query = query.filter_by(category_id=category_id)
    if start_date:
        query = query.filter(Expense.expense_date >= start_date)

    if end_date:
        query = query.filter(Expense.expense_date <= end_date)
    if min_value is not None:
        query = query.filter(Expense.amount >= min_value)

    if max_value is not None:
        query = query.filter(Expense.amount <= max_value)

    expenses = query.order_by(Expense.expense_date.desc()).paginate(
        page=page,
        per_page=3,
        error_out=False
    )
    categories = Category.query.all()

    return render_template(
        "expenses/index.html",
        expenses=expenses,
        stats=stats,
        search=search,
        selected_category=category_id,
        categories=categories,
        date_from=date_from,
        date_to=date_to,
        min_amount=min_amount,
        max_amount=max_amount
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
        expense_date = datetime.strptime(
                request.form["expense_date"],
                "%Y-%m-%d"
            ).date()
        expense = Expense(
            title = request.form['title'],
            amount = request.form['amount'],
            user_id=g.user.id,
            category_id=request.form['category_id'],
            expense_date=expense_date
        )
        db.session.add(expense)
        db.session.commit()
        flash("Expense added successfully.", constants.FLASH_SUCCESS)
        return redirect(url_for("expense.home"))
    return render_template("expenses/add.html", categories=categories, today=datetime.now().strftime("%Y-%m-%d"))

@expense_bp.route('/edit-expense/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=g.user.id
    ).first_or_404()
    categories = db.session.query(Category).all()
    if request.method == 'POST':
        expense_date = datetime.strptime(
                request.form["expense_date"],
                "%Y-%m-%d"
            ).date()
        expense.title = request.form["title"]
        expense.amount = request.form["amount"]
        expense.category_id = request.form["category_id"]
        expense.expense_date = expense_date

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

