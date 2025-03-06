from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for

from flask_login import login_required, current_user

from market.extensions import db
from market.forms import SubmitOrderForm
from market.models import BabyProducts, Beverages, FoodProducts, OrderDetails, Orders, PetProducts, Snacks

cart = Blueprint('cart', __name__)


@cart.route('/cart', methods=['GET', 'POST'])
@login_required
def cart_page():
    submission_form = SubmitOrderForm()
    is_ordered = Orders.query.filter_by(
        user_id=current_user.id).first().order_date is not None
    if request.method == "POST":
        # Update an existing order's date
        order = Orders.query.filter_by(user_id=current_user.id).first()
        order.order_date = datetime.now().strftime('%Y-%m-%d')
        db.session.commit()

        flash("Замовлення успішно записано, та скоро буде виконано!",
              category='success')
        return redirect(url_for('home_page'))
    elif request.method == "GET":
        # Get all IDs of chosen items
        order_details = OrderDetails.query.filter_by(
            order_id=current_user.id).first()
        product_id = order_details.product_id
        beverage_id = order_details.beverage_id
        baby_food_id = order_details.baby_food_id
        pet_id = order_details.pet_id
        snack_id = order_details.snack_id
        total_price = order_details.price

        # Get all chosen items
        product = FoodProducts.query.filter_by(id=product_id).first()
        beverage = Beverages.query.filter_by(id=beverage_id).first()
        baby_food = BabyProducts.query.filter_by(id=baby_food_id).first()
        pet_food = PetProducts.query.filter_by(id=pet_id).first()
        snack = Snacks.query.filter_by(id=snack_id).first()

        items = [product, beverage, baby_food, pet_food, snack]

        return render_template('cart.html', items=items, total_price=total_price,
                               submission_form=submission_form, is_ordered=is_ordered)
