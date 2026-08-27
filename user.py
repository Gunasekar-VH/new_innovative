from datetime import datetime
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.models import Book, Borrowing, User, db

user_bp = Blueprint("user", __name__, url_prefix="/user")


def user_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


@user_bp.route("/dashboard")
@user_required
def dashboard():
    user = User.query.get(session["user_id"])
    borrowed_count = Borrowing.query.filter_by(user_id=user.id, status="Borrowed").count()
    return render_template("user/dashboard.html", user=user, borrowed_count=borrowed_count)


@user_bp.route("/books")
@user_required
def books():
    term = request.args.get("q", "").strip()
    query = Book.query.order_by(Book.id.desc())
    if term:
        like = f"%{term}%"
        query = query.filter(
            (Book.title.ilike(like))
            | (Book.author.ilike(like))
            | (Book.category.ilike(like))
            | (Book.isbn.ilike(like))
        )
    return render_template("user/books.html", books=query.all())


@user_bp.route("/borrow/<int:book_id>", methods=["POST"])
@user_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available_quantity < 1:
        flash("Book unavailable.", "error")
        return redirect(url_for("user.books"))
    borrowing = Borrowing(user_id=session["user_id"], book_id=book.id, status="Borrowed")
    book.available_quantity -= 1
    db.session.add(borrowing)
    db.session.commit()
    flash("Book borrowed successfully.", "success")
    return redirect(url_for("user.borrowed_books"))


@user_bp.route("/borrowed")
@user_required
def borrowed_books():
    borrowings = Borrowing.query.filter_by(user_id=session["user_id"]).order_by(Borrowing.id.desc()).all()
    return render_template("user/borrowed_books.html", borrowings=borrowings)


@user_bp.route("/return/<int:borrowing_id>", methods=["POST"])
@user_required
def return_book(borrowing_id):
    borrowing = Borrowing.query.get_or_404(borrowing_id)
    if borrowing.user_id != session["user_id"]:
        flash("Unauthorized access.", "error")
        return redirect(url_for("user.borrowed_books"))
    if borrowing.status == "Returned":
        flash("This book was already returned.", "error")
        return redirect(url_for("user.borrowed_books"))
    borrowing.status = "Returned"
    borrowing.return_date = datetime.utcnow()
    borrowing.book.available_quantity += 1
    db.session.commit()
    flash("Book returned successfully.", "success")
    return redirect(url_for("user.borrowed_books"))


@user_bp.route("/profile")
@user_required
def profile():
    user = User.query.get(session["user_id"])
    return render_template("user/profile.html", user=user)
