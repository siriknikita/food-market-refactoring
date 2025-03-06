from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from market.extensions import db
from market.forms import LoginForm, RegisterForm
from market.models import OrderDetails, Orders, User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.username.data, email=form.email_address.data,
                              phone=form.phone.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        created_user = User.query.order_by(User.id.desc()).first()
        flash(f"Вітаємо, акаунт успішно створено! Тепер, ви авторизовані як: {
              user_to_create.name}!", category='success')
        new_order = Orders(user_id=created_user.id)
        db.session.add(new_order)
        db.session.commit()
        order_id = new_order.order_id
        order_details = OrderDetails(order_id=order_id)
        db.session.add(order_details)
        db.session.commit()
        return redirect(url_for('main.home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'УПС! Сталась помилка при створені користувача: {
                  err_msg}', category='danger')
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(name=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Успіх! Ви авторизовані як: {
                  attempted_user.name}', category='success')
            return redirect(url_for('main.home_page'))
        else:
            flash('УПС! Сталась помилка... Спробуйте ще раз!', category='danger')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("Ви більше не авторизовані!", category='info')
    return redirect(url_for("main.home_page"))
