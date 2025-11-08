import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import secrets

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://localhost:27017/car_rental")
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,      # Set True ONLY if your site is served over HTTPS!
    SESSION_COOKIE_SAMESITE="Lax"    # For best compatibility
)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

mongo = PyMongo(app)

# ========== UPLOAD ROUTE ==========
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ========== INDEX PAGE ==========
@app.route('/')
def index():
    return render_template('index.html')


# ========== HELPER: can_cancel ==========
def can_cancel(booking):
    today = datetime.now().date()
    start_date = datetime.strptime(booking['start'], "%Y-%m-%d").date()
    return booking.get('status') == 'active' and start_date >= today

# ========== USER ROUTES ==========

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('user_register'))
        if mongo.db.users.find_one({'email': email}):
            flash('Email already registered!')
            return redirect(url_for('user_register'))
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password
        })
        flash('Registration successful! Please log in.')
        return redirect(url_for('user_login'))
    return render_template('user_register.html')

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            session['user'] = {
                '_id': str(user['_id']),
                'name': user['name'],
                'email': user['email']
            }
            return redirect(url_for('user_home'))
        flash('Invalid email or password!')
        return redirect(url_for('user_login'))
    return render_template('user_login.html')

@app.route('/user/home')
def user_home():
    if 'user' not in session:
        return redirect(url_for('user_login'))
    # Get filter parameters
    brand = request.args.get('brand', '')
    seats = request.args.get('seats', '')
    fuel_type = request.args.get('fuel_type', '')
    max_rent = request.args.get('max_rent', '')
    # Build query
    query = {}
    if brand:
        query['brand'] = brand
    if seats:
        query['seats'] = int(seats)
    if fuel_type:
        query['fuel_type'] = fuel_type
    if max_rent:
        query['rent'] = {'$lte': float(max_rent)}
    # SOFT DELETE FILTER
    query['is_deleted'] = {'$ne': True}
    cars = list(mongo.db.cars.find(query))
    return render_template('user_home.html', cars=cars, user=session['user'])

@app.route('/user/dashboard')
def user_dashboard():
    if 'user' not in session:
        return redirect(url_for('user_login'))
    bookings = list(mongo.db.bookings.find({'user_id': session['user']['_id']}))
    for booking in bookings:
        booking['can_cancel'] = can_cancel(booking)
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('user_dashboard.html', bookings=bookings, current_time=today)

@app.route('/user/book/<car_id>', methods=['GET', 'POST'])
def book_car(car_id):
    if 'user' not in session:
        return redirect(url_for('user_login'))
    # SOFT DELETE FILTER
    car = mongo.db.cars.find_one({'_id': ObjectId(car_id), 'is_deleted': {'$ne': True}})
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        need_driver = request.form.get('driver') == 'yes'
        # Ensure valid dates
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
        if end_date < start_date:
            flash("End date cannot be before start date.")
            return redirect(url_for('book_car', car_id=car_id))
        days = (end_date - start_date).days
        if days < 1:
            days = 1
        car_cost = car['rent'] * days
        driver_cost = 500 * days if need_driver else 0
        total = car_cost + driver_cost
        booking = {
            'car': car,
            'user_id': session['user']['_id'],
            'user_name': session['user']['name'],
            'user_email': session['user']['email'],
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
            'days': days,
            'need_driver': need_driver,
            'car_cost': car_cost,
            'driver_cost': driver_cost,
            'total': total,
            'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'active'
        }
        result = mongo.db.bookings.insert_one(booking)
        mongo.db.cars.update_one({'_id': car['_id']}, {'$set': {'available': False}})
        return redirect(url_for('booking_receipt', booking_id=str(result.inserted_id)))
    return render_template('booking.html', car=car)

@app.route('/user/cancel_booking/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'user' not in session:
        return redirect(url_for('user_login'))
    booking = mongo.db.bookings.find_one({"_id": ObjectId(booking_id)})
    if not booking or booking.get('user_id') != session['user']['_id']:
        flash("Unauthorized.")
        return redirect(url_for('user_dashboard'))
    today = datetime.now().date()
    start_date = datetime.strptime(booking['start'], "%Y-%m-%d").date()
    if booking.get('status') != 'active':
        flash("Booking already cancelled or completed.")
        return redirect(url_for('user_dashboard'))
    if start_date < today:
        flash("Cannot cancel a booking that has started or completed.")
        return redirect(url_for('user_dashboard'))
    mongo.db.bookings.update_one({"_id": ObjectId(booking_id)}, {'$set': {'status': 'cancelled'}})
    mongo.db.cars.update_one({'brand': booking['car']['brand'], 'model': booking['car']['model']}, {'$set': {'available': True}})
    flash("Booking cancelled successfully.")
    return redirect(url_for('user_dashboard'))

@app.route('/user/receipt/<booking_id>')
def booking_receipt(booking_id):
    booking = mongo.db.bookings.find_one({'_id': ObjectId(booking_id)})
    return render_template('booking_receipt.html', booking=booking)

@app.route('/user/logout')
def user_logout():
    session.pop('user', None)
    return redirect(url_for('index'))

# ========== MANAGER ROUTES ==========
MANAGER_USER = os.environ.get("MANAGER_USER", "manager")
MANAGER_PASS = os.environ.get("MANAGER_PASS", "set_this_to_random")

@app.route('/manager/login', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == MANAGER_USER and password == MANAGER_PASS:
            session['manager'] = {'username': username}
            return redirect(url_for('manager_dashboard'))
        flash('Invalid manager credentials!')
        return redirect(url_for('manager_login'))
    return render_template('manager_login.html')

@app.route('/manager/dashboard')
def manager_dashboard():
    if 'manager' not in session:
        return redirect(url_for('manager_login'))
    # SOFT DELETE FILTER
    cars = list(mongo.db.cars.find({'is_deleted': {'$ne': True}}))
    bookings = list(mongo.db.bookings.find())
    current_rentals = []
    for car in cars:
        if not car.get("available", True):
            filtered = [b for b in bookings if b.get("car", {}).get("brand") == car.get("brand") and b.get("car", {}).get("model") == car.get("model")]
            if filtered:
                current_rentals.append({"car": car, "booking": filtered[-1]})
    return render_template("manager_dashboard.html",
        cars=cars,
        bookings=bookings,
        current_rentals=current_rentals
    )

@app.route('/manager/add_car', methods=['POST'])
def manager_add_car():
    if 'manager' not in session:
        return redirect(url_for('manager_login'))
    brand = request.form['brand']
    model = request.form['model']
    seats = int(request.form['seats'])
    rent = float(request.form['rent'])
    mileage = float(request.form['mileage'])
    fuel_type = request.form.get('fuel_type', 'Petrol')
    transmission = request.form.get('transmission', 'Manual')
    image = request.files.get('image')
    filename = None
    if image and image.filename:
       if allowed_file(image.filename):
          filename = secure_filename(image.filename)
          image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
       else:
          flash("Invalid image type! Allowed: png, jpg, jpeg, gif.")
          return redirect(request.url)

    mongo.db.cars.insert_one({
        'brand': brand,
        'model': model,
        'seats': seats,
        'rent': rent,
        'mileage': mileage,
        'fuel_type': fuel_type,
        'transmission': transmission,
        'image': filename,
        'available': True,
        'is_deleted': False
    })
    flash('Car added successfully!')
    return redirect(url_for('manager_dashboard'))

@app.route('/manager/edit_car/<car_id>', methods=['GET', 'POST'])
def manager_edit_car(car_id):
    if 'manager' not in session:
        return redirect(url_for('manager_login'))
    # SOFT DELETE FILTER
    car = mongo.db.cars.find_one({'_id': ObjectId(car_id), 'is_deleted': {'$ne': True}})
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        seats = int(request.form['seats'])
        rent = float(request.form['rent'])
        mileage = float(request.form['mileage'])
        fuel_type = request.form.get('fuel_type', 'Petrol')
        transmission = request.form.get('transmission', 'Manual')
        available = request.form.get('available') == 'on'
        image = request.files.get('image')
        filename = car.get('image')
        if image and image.filename:
            if allowed_file(image.filename):
               filename = secure_filename(image.filename)
               image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
               flash("Invalid image type! Allowed: png, jpg, jpeg, gif.")
               return redirect(request.url)

        mongo.db.cars.update_one({'_id': ObjectId(car_id)}, {'$set': {
            'brand': brand,
            'model': model,
            'seats': seats,
            'rent': rent,
            'mileage': mileage,
            'fuel_type': fuel_type,
            'transmission': transmission,
            'image': filename,
            'available': available
        }})
        flash('Car updated successfully!')
        return redirect(url_for('manager_dashboard'))
    return render_template('edit_car.html', car=car)

@app.route('/manager/delete_car/<car_id>')
def manager_delete_car(car_id):
    if 'manager' not in session:
        return redirect(url_for('manager_login'))
    # SOFT DELETE!
    mongo.db.cars.update_one({'_id': ObjectId(car_id)}, {'$set': {'is_deleted': True}})
    flash('Car deleted successfully!')
    return redirect(url_for('manager_dashboard'))

@app.route('/manager/logout')
def manager_logout():
    session.pop('manager', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
