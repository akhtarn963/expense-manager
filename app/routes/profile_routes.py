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
from app.models import  db
from app.decorators import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import constants

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/profile")
@login_required
def profile():
    return render_template("profile/index.html")

@profile_bp.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        g.user.name = request.form["name"].strip()
        """ g.user.email = request.form["email"].strip().lower() """
        db.session.commit()
        flash("Profile updated successfully.", constants.FLASH_SUCCESS)
        return redirect(url_for("profile.profile"))

    return render_template("profile/edit.html")

@profile_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]
        if not check_password_hash(g.user.password, old_password):
            flash("Invalid old password.", constants.FLASH_DANGER)
            return redirect(url_for("profile.profile"))
        if new_password == old_password:
            flash("New password cannot be the same as the old password.", FLASH_DANGER)
            return redirect(url_for("profile.profile"))
        if new_password != confirm_password:
            flash("New passwords do not match.", constants.FLASH_DANGER)
            return redirect(url_for("profile.profile"))
        g.user.password = generate_password_hash(new_password)
        db.session.commit()
        flash("Password updated successfully.", constants.FLASH_SUCCESS)
        return redirect(url_for("profile.profile"))
    return render_template("profile/change_password.html")