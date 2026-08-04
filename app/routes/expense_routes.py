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

expense_bp = Blueprint("expense", __name__)

@expense_bp.route("/")
@login_required
def home():  
    expenses = Expense.query.filter_by(user_id=g.user.id).all()
    stats = calculate_statistics(expenses)
    
    return render_template(
        "home.html",
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
            flash("Please select a category.", "danger")
            return redirect(url_for("expense.add_expense"))
        expense = Expense(
            title = request.form['title'],
            amount = request.form['amount'],
            user_id=g.user.id,
            category_id=request.form['category_id']
        )
        db.session.add(expense)
        db.session.commit()
        flash("Expense added successfully.", "success")
        return redirect(url_for("expense.home"))
    return render_template("add_expense.html", categories=categories)

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
        flash("Expense updated successfully.", "success")
        return redirect(url_for("expense.home"))

    return render_template("edit_expense.html", expense=expense, categories=categories)

@expense_bp.route('/delete-expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    
    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=g.user.id
    ).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully.", "success")
    return redirect(url_for("expense.home"))

@expense_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@expense_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        g.user.name = request.form["name"].strip()
        """ g.user.email = request.form["email"].strip().lower() """
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("expense.profile"))

    return render_template("edit_profile.html")

@expense_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    old_password = request.form["old_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]
    if not check_password_hash(g.user.password, old_password):
        flash("Invalid old password.", "danger")
        return redirect(url_for("expense.profile"))
    if new_password == old_password:
        flash("New password cannot be the same as the old password.", "danger")
        return redirect(url_for("expense.profile"))
    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("expense.profile"))
    g.user.password = generate_password_hash(new_password)
    db.session.commit()
    flash("Password updated successfully.", "success")
    return redirect(url_for("expense.profile"))