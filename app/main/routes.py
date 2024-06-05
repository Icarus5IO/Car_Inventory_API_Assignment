from flask import render_template, redirect, url_for, abort, flash, request
from flask_login import login_required, current_user
from app.main import main
from app.models import Car, db 
from app.main.forms import CarForm


@main.route('/')
def index():
    cars = None
    forms = {}  # Dictionary to store forms for each car
    if current_user.is_authenticated:
        cars = current_user.cars
        for car in cars:
            forms[car.id] = CarForm()  # Create a form for each car
    return render_template('index.html', title='Car Inventory', cars=cars, forms=forms)



@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Your Profile')


@main.route('/create_car', methods=['GET', 'POST'])
@login_required
def create_car():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(
            make=form.make.data,
            model=form.model.data,
            year=form.year.data,
            color=form.color.data,
            transmission=form.transmission.data,
            user_id=current_user.id
        )
        db.session.add(car)
        db.session.commit()
        flash('Car added to inventory!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_car.html', title='Add New Car', form=form)


@main.route('/update_car/<int:car_id>', methods=['GET', 'POST'])
@login_required
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)  # Forbidden - User doesn't own this car
    form = CarForm()
    if form.validate_on_submit():
        # Update the car object with data from the form
        car.make = form.make.data
        car.model = form.model.data
        car.year = form.year.data
        car.color = form.color.data
        car.transmission = form.transmission.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        # Populate the form with existing car data
        form.make.data = car.make
        form.model.data = car.model
        form.year.data = car.year
        form.color.data = car.color
        form.transmission.data = car.transmission
    return render_template('update_car.html', title='Edit Car', form=form, car=car)


@main.route('/delete_car/<int:car_id>', methods=['POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        abort(403)  # Forbidden - User doesn't own this car
    db.session.delete(car)
    db.session.commit()
    flash('Car has been deleted.', 'success')
    return redirect(url_for('main.index'))


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403