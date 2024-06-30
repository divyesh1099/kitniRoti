from flask import Flask, jsonify, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, MealForm
from app.models import User, Meal, UserMeal
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, time

@app.route("/register", methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in"}), 400
    form = RegistrationForm()
    form.populate_from_json(request.json)
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": f"Account created for {form.username.data}!"}), 201
    return jsonify(form.errors), 400

@app.route("/login", methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({"message": "Already logged in"}), 400
    form = LoginForm()
    form.populate_from_json(request.json)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Login unsuccessful. Please check email and password"}), 401
    return jsonify(form.errors), 400

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route("/meal/new", methods=['POST'])
@login_required
def new_meal():
    form = MealForm()
    form.populate_from_json(request.json)
    if form.validate_on_submit():
        meal = Meal(meal_type=form.meal_type.data, rotis=form.rotis.data, sabjis=form.sabjis.data, rice=form.rice.data, special_dish=form.special_dish.data, milk=form.milk.data, chef=current_user)
        db.session.add(meal)
        db.session.commit()
        return jsonify({"message": "Meal has been added!"}), 201
    return jsonify(form.errors), 400

@app.route("/meals")
@login_required
def view_meals():
    meals = Meal.query.all()
    meals_data = []
    for meal in meals:
        meals_data.append({
            'id': meal.id,
            'date': meal.date,
            'meal_type': meal.meal_type,
            'rotis': meal.rotis,
            'sabjis': meal.sabjis,
            'rice': meal.rice,
            'special_dish': meal.special_dish,
            'milk': meal.milk,
            'chef': meal.chef.username,
            'created_at': meal.created_at,
            'updated_at': meal.updated_at
        })
    return jsonify(meals_data), 200

@app.route("/meals/current", methods=['GET'])
def current_meal():
    current_date = datetime.utcnow().date()
    current_time = datetime.utcnow().time()
    
    if time(5, 0) <= current_time < time(10, 0):
        meal_type = 'Breakfast'
    elif time(10, 0) <= current_time < time(15, 0):
        meal_type = 'Lunch'
    else:
        meal_type = 'Dinner'
        
    meal = Meal.query.filter_by(date=current_date, meal_type=meal_type).first()
    if not meal:
        return jsonify({"message": "No meal found for this time."}), 404
    
    meal_data = {
        'meal_type': meal.meal_type,
        'rotis': meal.rotis,
        'sabjis': meal.sabjis,
        'rice': meal.rice,
        'special_dish': meal.special_dish,
        'milk': meal.milk,
        'chef': meal.chef.username
    }
    return jsonify(meal_data), 200

@app.route("/meal/<int:meal_id>", methods=['GET'])
@login_required
def get_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    meal_data = {
        'id': meal.id,
        'date': meal.date,
        'meal_type': meal.meal_type,
        'rotis': meal.rotis,
        'sabjis': meal.sabjis,
        'rice': meal.rice,
        'special_dish': meal.special_dish,
        'milk': meal.milk,
        'chef': meal.chef.username,
        'created_at': meal.created_at,
        'updated_at': meal.updated_at
    }
    return jsonify(meal_data), 200

@app.route("/meal/<int:meal_id>", methods=['PUT'])
@login_required
def update_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    form = MealForm()
    form.populate_from_json(request.json)
    if form.validate_on_submit():
        meal.meal_type = form.meal_type.data
        meal.rotis = form.rotis.data
        meal.sabjis = form.sabjis.data
        meal.rice = form.rice.data
        meal.special_dish = form.special_dish.data
        meal.milk = form.milk.data
        db.session.commit()
        return jsonify({"message": "Meal has been updated!"}), 200
    return jsonify(form.errors), 400

@app.route("/meal/<int:meal_id>", methods=['DELETE'])
@login_required
def delete_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": "Meal has been deleted!"}), 200

@app.route("/user_meal/<int:meal_id>", methods=['POST'])
@login_required
def add_user_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    data = request.json
    rotis = data.get('rotis', 0)
    
    user_meal = UserMeal.query.filter_by(user_id=current_user.id, meal_id=meal_id).first()
    if user_meal:
        return jsonify({"message": "User meal already exists. Use PUT to update."}), 400
    
    user_meal = UserMeal(user_id=current_user.id, meal_id=meal_id, rotis=rotis)
    db.session.add(user_meal)
    db.session.commit()
    return jsonify({"message": "User meal has been added!"}), 201

@app.route("/user_meal/<int:meal_id>", methods=['PUT'])
@login_required
def update_user_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    data = request.json
    rotis = data.get('rotis', 0)
    
    user_meal = UserMeal.query.filter_by(user_id=current_user.id, meal_id=meal_id).first()
    if not user_meal:
        return jsonify({"message": "User meal not found. Use POST to create."}), 404
    
    user_meal.rotis = rotis
    db.session.commit()
    return jsonify({"message": "User meal has been updated!"}), 200

@app.route("/chef/rotis/<int:meal_id>", methods=['GET'])
@login_required
def get_total_rotis(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    if meal.user_id != current_user.id:
        return jsonify({"message": "Only the chef can see the total rotis."}), 403
    
    total_rotis = db.session.query(db.func.sum(UserMeal.rotis)).filter_by(meal_id=meal_id).scalar()
    return jsonify({"total_rotis": total_rotis}), 200

@app.route("/users", methods=['GET'])
@login_required
def view_users():
    users = User.query.all()
    users_data = []
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    return jsonify(users_data), 200

@app.route("/user/<int:user_id>", methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email
    }
    return jsonify(user_data), 200

@app.route("/user/<int:user_id>", methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    form = RegistrationForm()
    form.populate_from_json(request.json)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.commit()
        return jsonify({"message": "User has been updated!"}), 200
    return jsonify(form.errors), 400

@app.route("/user/<int:user_id>", methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User has been deleted!"}), 200

@app.route("/meals/filter", methods=['GET'])
@login_required
def filter_meals():
    query = Meal.query

    date = request.args.get('date')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    meal_type = request.args.get('meal_type')

    if date:
        query = query.filter(Meal.date == date)

    if start_date and end_date:
        query = query.filter(Meal.date.between(start_date, end_date))

    if meal_type:
        query = query.filter(Meal.meal_type == meal_type)

    meals = query.all()
    meals_data = []
    for meal in meals:
        meals_data.append({
            'id': meal.id,
            'date': meal.date,
            'meal_type': meal.meal_type,
            'rotis': meal.rotis,
            'sabjis': meal.sabjis,
            'rice': meal.rice,
            'special_dish': meal.special_dish,
            'milk': meal.milk,
            'chef': meal.chef.username,
            'created_at': meal.created_at,
            'updated_at': meal.updated_at
        })
    return jsonify(meals_data), 200
