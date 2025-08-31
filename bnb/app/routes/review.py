from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.property import Property
from app.models.review import Review

review_bp = Blueprint("review", __name__)

# ---------------- Add Review ----------------
@review_bp.route("/property/<int:property_id>/review", methods=["POST"])
@login_required
def add_review(property_id):
    property_obj = Property.query.get_or_404(property_id)

    # Prevent owner from reviewing own property
    if current_user.id == property_obj.host_id:
        flash("You cannot review your own property.", "danger")
        return redirect(url_for("property.view_property", property_id=property_id))

    rating = request.form.get("rating")
    comment = request.form.get("comment")

    if not rating or not comment:
        flash("Please provide both rating and comment.", "warning")
        return redirect(url_for("property.view_property", property_id=property_id))

    # Check if user already has a review
    existing_review = Review.query.filter_by(property_id=property_id, user_id=current_user.id).first()

    if existing_review:
        flash("You have already reviewed this property.", "info")
    else:
        new_review = Review(
            rating=int(rating),
            comment=comment,
            property_id=property_id,
            user_id=current_user.id,
        )
        db.session.add(new_review)
        db.session.commit()
        flash("Review added successfully!", "success")

    return redirect(url_for("property.view_property", property_id=property_id))


# ---------------- Edit Review ----------------
@review_bp.route("/review/<int:review_id>/edit", methods=["GET", "POST"])
@login_required
def edit_review(review_id):
    review_obj = Review.query.get_or_404(review_id)

    if review_obj.user_id != current_user.id:
        flash("You cannot edit someone else's review.", "danger")
        return redirect(url_for("property.view_property", property_id=review_obj.property_id))

    if request.method == "POST":
        review_obj.rating = int(request.form.get("rating"))
        review_obj.comment = request.form.get("comment")
        db.session.commit()
        flash("Review updated successfully!", "success")
        return redirect(url_for("property.view_property", property_id=review_obj.property_id))

    return render_template("edit_review.html", review=review_obj)


# ---------------- Delete Review ----------------
@review_bp.route("/review/<int:review_id>/delete", methods=["POST"])
@login_required
def delete_review(review_id):
    review_obj = Review.query.get_or_404(review_id)

    if review_obj.user_id != current_user.id:
        flash("You cannot delete someone else's review.", "danger")
        return redirect(url_for("property.view_property", property_id=review_obj.property_id))

    db.session.delete(review_obj)
    db.session.commit()
    flash("Review deleted successfully.", "success")
    return redirect(url_for("property.view_property", property_id=review_obj.property_id))
