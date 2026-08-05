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

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def home():  
    expenses = Expense.query.filter_by(user_id=g.user.id).all()
    stats = calculate_statistics(expenses)
    
    return render_template(
        "dashboard/index.html",
        expenses=expenses,
        stats=stats
    )