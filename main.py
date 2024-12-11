import os
import binascii

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

from data import data
from data.base import create_db
from data.data_to_db import write_data_to_db
from data.base import Session
from data.forms import SingUpForm, LoginForm
from data.models import User, Tour


app = Flask(__name__)
app.secret_key = binascii.hexlify(os.urandom(24))
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Для купівлі туру спочатку увійдіть у систему"
login_manager.init_app(app)


@app.context_processor
def context():
    with Session() as session:
        user = session.query(User).where(User.id == (current_user.id if current_user.is_authenticated else 0)).first()
        tours = session.query(Tour).all()
        return dict(tours=tours, departures=data.departures, user=user, user_tours=user.tours if user else [])


@login_manager.user_loader
def load_user(user_id: int):
    with Session() as session:
        return session.query(User).where(User.id == user_id).first()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/tour/<int:tour_id>/")
def get_tour(tour_id):
    with Session() as session:
        tour = session.query(Tour).where(Tour.id == tour_id).first()
        return render_template("tour.html", tour=tour)


@app.get("/departure/<dep_eng>/")
def departure(dep_eng):
    with Session() as session:
        tours = session.query(Tour).where(Tour.departure == dep_eng).all()
        return render_template("departure.html", tours=tours)


@app.get("/tour/reserve/<int:tour_id>/")
@login_required
def reserve(tour_id):
    with Session() as session:
        user = session.query(User).where(User.id == current_user.id).first()
        tour = session.query(Tour).where(Tour.id == tour_id).first()
        user.tours.append(tour)
        session.commit()
        flash(f"Тур: '{tour.title}' успішно заброньовано")
        return redirect(url_for("index"))


@app.route("/singup/", methods=["GET", "POST"])
def singup():
    singup_form = SingUpForm()
    if singup_form.validate_on_submit():
        with Session() as session:
            user = session.query(User).where(User.email == singup_form.email.data).first()
            if user:
                flash("Користувач з такою електронною поштою вже зареєстрований в системі")
                return redirect(url_for("login"))

            password = generate_password_hash(singup_form.password.data)
            user = User(
                username=singup_form.username.data,
                email=singup_form.email.data,
                password=password
            )
            session.add(user)
            session.commit()
            flash("Вітаю, Ви успішно зареєструвались")
            return redirect(url_for("login"))

    return render_template("singup.html", form=singup_form, departures=data.departures)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    print(f"{form.username.data = }")
    print(f"{form.validate_on_submit() = }")
    if form.validate_on_submit():
        username = form.username.data

        with Session() as session:
            user = session.query(User).where(or_(User.username == username, User.email == username)).first()

            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for("account"))

                flash("Невірний пароль")
                return redirect(url_for("login"))

            flash("Такого користувача немає у системі")
            return redirect(url_for("singup"))

    return render_template("login.html", form=form)


@app.get("/account/")
@login_required
def account():
    return render_template("account.html")


@app.get("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    create_db()
    # write_data_to_db()
    app.run(debug=True)
