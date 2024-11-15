from flask import Flask, request, redirect, render_template, redirect, url_for
import json
app = Flask(__name__)


def create_file():
    with open("info.json", "w") as file:
        json.dump({
                "total_balance":0, "food":0, "house_hold":0, "clothing":0,
                "personal_expense":0, "subscription":0,"housing_expense":0,
                "insurance":0,"other":0}, file)


create_file()


@app.route('/add_balance', methods=['GET', 'POST'])
def add_balance():
    return render_template("main.html")


@app.route('/', methods=['GET', 'POST'])
def about():
    return render_template("about.html")


@app.route('/initialize_balance', methods=['GET', 'POST'])
def initialize_balance():
    # get the data and save it in the json
    json_data = get_data()
    request_data = request.form
    print(request_data)

    write_data(request_data, json_data)

    return redirect(url_for('about'))


@app.route('/spend_balance')
def spend_balance_page():
    json_data = get_data()
    return render_template("spendBalance.html", json_data=json_data)


@app.route('/spend/<category>', methods=['GET', 'POST'])
def spend_money(category):
    # get data of category and the amount and modify the json
    json_data = get_data()
    request_data = request.form
    print(request_data)
    useMoney(request_data, json_data, category)
    return redirect(url_for('spend_balance_page'))
    


@app.route('/checkBalance', methods=['GET'])
def checkBalance():
    json_data = get_data()
    # return some kind get_data
    return render_template('checkBalance.html', json_data=json_data)


def write_data(request_data, json_data):
    sent = True
    check = 0.00
    categories = ['total_balance', 'food', 'house_hold', 'clothing', 
                'personal_expense', 'subscription',
                'housing_expense', 'insurance', 'other']
    total_balance = request_data.get('total_balance')
    total_balance = "{:.2f}".format(float(total_balance))
    json_data['total_balance'] = total_balance
    # while True:
        
        # break
        # if is_float(total_balance):
        #     json_data['total_balance'] = total_balance
        #     break
        # else:
        #     print("Please input an integer or float")

    while sent:
        for c in range(1, len(categories)):
            if categories[c] == 'other':
                total_balance = float(total_balance)
                json_data['other'] = "{:.2f}".format(float(total_balance - check))
                sent = False
                break
            while True:
                expense = request_data.get(categories[c])
                if is_float(expense):
                    json_data[categories[c]] = "{:.2f}".format(float(expense))
                    check += float(expense)
                    break
                else:
                    print("Error entering value")
                    break
            if check > float(json_data['total_balance']):
                print("Your budgeting exceeded the total budget, please re-enter all the values again")
                check = 0
                break
    with open("info.json", "w") as file:
        json.dump(json_data, file)


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


def useMoney(request_data, json_data, category):
    while True:        
        if category not in json_data:
            print(f"Category '{category}' does not exist. Please try again.")
            continue  # Continue to prompt for a valid category

        break  # Exit the loop if the category is valid

    while True:
        expense = "{:.2f}".format(float(request_data.get(category)))
        expense = float(expense)

        if is_float(expense):
            expense = float(expense)
            break
        else:
            print("Invalid amount entered. Please enter a valid number.")

    category_budget = "{:.2f}".format(float((json_data[category])))
    category_budget = float(category_budget)
    if category_budget - expense >= 0:
        json_data[category] = "{:.2f}".format(float(category_budget) - float(expense))
        json_data['total_balance'] = "{:.2f}".format(float(json_data['total_balance']) - (float(expense)))
        with open("info.json", "w") as file:
            json.dump(json_data, file)
    else:
        print(f"Insufficient funds in {category}. You have ${category_budget:.2f} left.")


if __name__ == "__main__":
    app.run(debug=True)