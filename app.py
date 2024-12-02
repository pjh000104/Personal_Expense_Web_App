from flask import Flask, request, redirect, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Expense
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

def create_file():
    with open("info.json", "w") as file:
        json.dump({
                "total_balance":0, "food":0, "house_hold":0, "clothing":0,
                "personal_expense":0, "subscription":0,"housing_expense":0,
                "insurance":0,"other":0}, file)


create_file()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return "User with this email already exists!"

        # Create new user
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('about'))
        else:
            return "Invalid credentials!"

    return render_template('login.html')



@app.route('/add_balance', methods=['GET', 'POST'])
def add_balance():
    return render_template("main.html")


@app.route('/', methods=['GET', 'POST'])
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("about.html")


@app.route('/initialize_balance', methods=['GET', 'POST'])
def initialize_balance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # get the data and save it in the json
    user_id = session['user_id']
    user = User.query.get(user_id)

    if not user.expenses:
        new_expense = Expense(user_id=user_id)
        db.session.add(new_expense)
        db.session.commit()

    request_data = request.form
    write_data(request_data)
    return redirect(url_for('about'))


@app.route('/spend_balance')
def spend_balance_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    balances = Expense.query.filter_by(user_id=user_id).first()

    if not balances:
        return "No balances found. Please initialize them first."

    return render_template("spendBalance.html", balances=balances)


@app.route('/spend/<category>', methods=['GET', 'POST'])
def spend_money(category):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # get data of category and the amount and modify the json
    request_data = request.form
    print(request_data)
    useMoney(request_data, category)
    return redirect(url_for('spend_balance_page'))



@app.route('/checkBalance', methods=['GET'])
def checkBalance():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    balances = Expense.query.filter_by(user_id=user_id).first()

    if not balances:
        return "No balances found. Please initialize them first."

    return render_template('checkBalance.html', balances=balances)


def write_data(request_data):
    sent = True
    check = 0.00
    categories = ['total_balance', 'food', 'house_hold', 'clothing', 
                'personal_expense', 'subscription', 'housing_expense', 
                'insurance', 'other']

    # Get total_balance from request data and format it to 2 decimal places
    total_balance = request_data.get('total_balance')
    total_balance = "{:.2f}".format(float(total_balance))  # Format total_balance to 2 decimal places

    user_id = session['user_id']
    # Fetch the existing Expense object for the user
    expenses = Expense.query.filter_by(user_id=user_id).first()

    expenses.total_balance = total_balance
    # Start looping to fill out the categories
    while sent:
        for c in range(1, len(categories)):  # Start at index 1 to skip the 'total_balance' category
            category = categories[c]

            # Handle the special case for 'other' category
            if category == 'other':
                total_balance = float(total_balance)  # Ensure total_balance is a float
                # Deduct check (sum of already allocated expenses) from total_balance and set the 'other' value
                expenses.other = "{:.2f}".format(float(total_balance - check))
                sent = False  # Exit the loop once 'other' category is processed
                break

            # Process regular categories (food, house_hold, etc.)
            while True:
                expense = request_data.get(category)  # Get value for current category
                if is_float(expense):  # Ensure the value is a valid float
                    formatted_expense = "{:.2f}".format(float(expense))
                    setattr(expenses, category, formatted_expense)  # Dynamically set the attribute on the model
                    check += float(expense)  # Add expense value to the total
                    break  # Exit inner loop to continue with the next category
                else:
                    print(f"Error entering value for {category}. Please enter a valid number.")
                    break  # Exit the loop and ask user to re-enter the value for that category

            # If the sum of expenses exceeds total_balance, ask the user to re-enter the values
            if check > float(total_balance):
                print("Your budgeting exceeded the total budget, please re-enter all the values again.")
                check = 0  # Reset check to zero
                return redirect(url_for('add_balance'))  # Redirect to the balance input page

        # Commit the changes to the database after all categories have been processed
        db.session.commit()


@app.route('/check_balances', methods=['GET'])
def check_balances():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    balances = Expense.query.filter_by(user_id=user_id).first()

    if not balances:
        return "No balances found. Please initialize them first."

    return render_template('check_balances.html', balances=balances)

def is_float(value):
    try:
        # Try to convert the value to a float
        float(value)
        return True
    except ValueError:
        # If conversion fails, it's not a float
        return False


def create_file():
    with open("info.json", "w") as file:
        json.dump({
                "total_balance": 0, "food": 0, "house_hold": 0, "clothing": 0,
                "personal_expense": 0, "subscription": 0, "housing_expense": 0,
                "insurance": 0, "other": 0}, file)  
      

# A function which return's the dictionary/hashmap within the file          
def get_data():
    with open('info.json', 'r') as file:
        data = json.load(file)
        return data


def useMoney(request_data, category):
    categories = ['total_balance', 'food', 'house_hold', 'clothing', 
            'personal_expense', 'subscription', 'housing_expense', 
            'insurance', 'other']
    
    user_id = session['user_id']
    expenses = Expense.query.filter_by(user_id=user_id).first()
    
    while True:        
        if category not in categories:
            print(f"Category '{category}' does not exist. Please try again.")
            continue  # Continue to prompt for a valid category

        break  # Exit the loop if the category is valid

    expense = request_data.get(category)  # Get value for current category
    category_budget = "{:.2f}".format((getattr(expenses,category)))
    print("printing category budget: " + category_budget)
    print("printing expense: " + expense)
    if float(category_budget) - float(expense) >= 0:
        setattr(expenses, category, (float(category_budget) - float(expense)))
        expenses.total_balance = "{:.2f}".format(expenses.total_balance - float(expense))
        db.session.commit()
    else:
        print(f"Insufficient funds in {category}. You have ${category_budget} left.")


if __name__ == "__main__":
    app.run(debug=True)
