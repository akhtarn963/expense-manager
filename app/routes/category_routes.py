from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    g
)
from app.models import Category, db
from app.decorators import login_required

category_bp = Blueprint("category", __name__)

@category_bp.route("/categories")
@login_required
def list_categories():
    categories = Category.query.all()
    return render_template("categories/index.html", categories=categories)

@category_bp.route("/add-category", methods=["GET", "POST"])
@login_required
def add_category():
    if request.method == "POST":
        name = request.form["name"].strip()
        search_name = request.form["name"].strip().lower()

        existing_category = Category.query.filter(
                                db.func.lower(Category.name) == search_name
                            ).first()
        if existing_category:
            flash("Category already exists.", "warning")
            return redirect(url_for("category.add_category"))
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash("Category added successfully.", "success")
        return redirect(url_for("category.list_categories"))
    return render_template("categories/add.html")

@category_bp.route("/edit-category/<int:category_id>", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    category = db.get_or_404(Category, category_id)
    if request.method == "POST":
        name = request.form["name"].strip()
        search_name = name.lower()
        existing_category = Category.query.filter(
            db.func.lower(Category.name) == search_name
        ).first()
        if existing_category and existing_category.id != category_id:
            flash("Category already exists.", "warning")
            return redirect(url_for("category.edit_category", category_id=category_id))
        category.name = name
        db.session.commit()
        flash("Category updated successfully.", "success")
        return redirect(url_for("category.list_categories"))
    return render_template("categories/edit.html", category=category)

@category_bp.route("/delete-category/<int:category_id>", methods=["POST"])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted successfully.", "success")
    return redirect(url_for("category.list_categories"))
