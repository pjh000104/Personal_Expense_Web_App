from flask import Flask, request, redirect, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Expense
import json
import pygame
import random


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
    user_id = session['user_id']
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("about.html")


@app.route('/initialize_balance', methods=['GET', 'POST'])
def initialize_balance():
    # get the data and save it in the json
    user_id = session['user_id']
    user = User.query.get(user_id)
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if not user.expenses:
        new_expense = Expense(user_id=user_id)
        db.session.add(new_expense)
        db.session.commit()

    request_data = request.form
    write_data(request_data)
    return redirect(url_for('about'))


@app.route('/spend_balance')
def spend_balance_page():
    user_id = session['user_id']
    if 'user_id' not in session:
        return redirect(url_for('login'))
    balances = Expense.query.filter_by(user_id=user_id).first()

    if not balances:
        return "No balances found. Please initialize them first."

    return render_template("spendBalance.html", balances=balances)


@app.route('/spend/<category>', methods=['GET', 'POST'])
def spend_money(category):
    user_id = session['user_id']
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # get data of category and the amount and modify the json
    request_data = request.form
    print(request_data)
    useMoney(request_data, category)
    return redirect(url_for('spend_balance_page'))



@app.route('/checkBalance', methods=['GET'])
def checkBalance():
    user_id = session['user_id']
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    balances = Expense.query.filter_by(user_id=user_id).first()

    if not balances:
        return "No balances found. Please initialize them first."
    
    return render_template('checkBalance.html', balances=balances)

@app.route('/snake_game')
def snake_game():
    startgame()
    return redirect(url_for('about'))

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


def startgame():
    
    pygame.init()
    # Colors
    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    # Display settings
    dis_width = 600
    dis_height = 400
    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Snake by Hiruy')

    # Timing and speed
    clock = pygame.time.Clock()
    snake_block = 10
    initial_speed = 15

    # Fonts
    font_style = pygame.font.SysFont("italic", 25)
    score_font = pygame.font.SysFont("Helvetica", 35)

    def Your_score(score):
        value = score_font.render("Your Score: " + str(score), True, white)
        dis.blit(value, [0, 0])

    def our_snake(snake_block, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

    def message(msg, color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [dis_width / 6, dis_height / 3])

    #Obstacles
    def draw_obstacles(obstacle_list):
        for obstacle in obstacle_list:
            pygame.draw.rect(dis, red, [obstacle[0], obstacle[1], snake_block, snake_block])

    def gameLoop():
        game_over = False
        game_close = False

        # Snake initial position
        x1 = dis_width / 2
        y1 = dis_height / 2

        # Snake movement
        x1_change = 0
        y1_change = 0

        # Snake details
        snake_List = []
        Length_of_snake = 1

        # Initial food location
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        # Initial Obstacles
        obstacles = []
        for _ in range(5):  # Change the number of obstacles here
            obstacles.append([random.randrange(1, (dis_width // 10)) * 10, random.randrange(1, (dis_height // 10)) * 10])

        # Game speed
        snake_speed = initial_speed

        while not game_over:

            while game_close:
                dis.fill(blue)
                message("You Lost! Press C-Play Again or Q-Quit", red)
                Your_score(Length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            gameLoop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = snake_block
                        x1_change = 0

            # Update snake position
            x1 += x1_change
            y1 += y1_change

            # Fill background and draw food
            dis.fill(blue)
            pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

            # Check for border collision
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True

            # Snake mechanics
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)

            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            # Check for self collision
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True

            # Draw snake and obstacles
            our_snake(snake_block, snake_List)
            draw_obstacles(obstacles)

            # Score display
            Your_score(Length_of_snake - 1)

            # Display update
            pygame.display.update()

            # Eating food
            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                Length_of_snake += 1
                snake_speed += 1  # Increase speed as the snake eats more

            # Check collision with obstacles
            for obstacle in obstacles:
                if x1 == obstacle[0] and y1 == obstacle[1]:
                    game_close = True

            # Update game based on the snake's speed
            clock.tick(snake_speed)

        pygame.quit()
        # quit()
    gameLoop()

if __name__ == "__main__":
    app.run(debug=True)
