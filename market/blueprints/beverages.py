from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import login_required, current_user
from market import db
from market.forms import AddingForm
from market.models import Beverages, Categories, OrderDetails

beverages = Blueprint('beverages', __name__)


@beverages.route('/beverages', methods=['GET', 'POST'])
@login_required
def beverages_page():
    adding_form = AddingForm()
    if request.method == "POST":
        # Get chosen item from user
        added_item = request.form.get('added_item')
        added_item_object = Beverages.query.filter_by(name=added_item).first()
        if added_item_object:
            current_user_id = current_user.id
            order_detail = OrderDetails.query.filter_by(
                order_id=current_user_id).first()
            # Update an existing ID field
            order_detail.beverage_id = added_item_object.id
            # Update the price to pay
            if order_detail.price is None:
                order_detail.price = 0
            order_detail.price += added_item_object.price
            db.session.commit()

            flash(
                f"Товар '{added_item_object.name}' додано до кошика!", category='success')

            if order_detail and order_detail.all_fields_have_values():
                flash("Ваш кошик повний! Хочете зробити замовлення?",
                      category='info')
                return redirect(url_for('cart_page'))
        return redirect(url_for('home_page'))
    elif request.method == "GET":
        items = Beverages.query.all()
        category_id = Beverages.category_id
        category = Categories.query.filter_by(id=category_id).first()
        return render_template('beverages.html', items=items, category=category,
                               adding_form=adding_form)
