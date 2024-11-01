from flask import Flask, request, redirect, render_template
import json
app = Flask(__name__)


def create_file():
    with open("info.json", "w") as file:
        json.dump({
                "total_balance":0, "food":0, "house_hold":0, "clothing":0,
                "personal_expense":0, "subscription":0,"housing_expense":0,
                "insurance":0,"other":0}, file)


create_file()


@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template("index.html")


@app.route('/initialize_balance', methods=['GET', 'POST'])
def initialize_balance():
    # get the data and save it in the json
    json_data = get_data()
    request_data = request.form
    write_data(request_data, json_data)


    
    return render_template("index.html")



@app.route('/spend', methods=['GET', 'POST'])
def spend_money():
    # get data of category and the amount and modify the json
    return


@app.route('/check_balance', methods=['GET'])
def check_balance():
    # return some kind get_data
    return



def start_software():
    create_file()
    data = get_data()

    sent = True
    check = 0

    categories = ['total_balance', 'food', 'house_hold', 'clothing', 
                  'personal_expense', 'subscription',
                  'housing_expense', 'insurance', 'other']

    print("Hello welcome to the Personal_Expense")

    while True:
        total_balance = input("What is your total budget for this month: " )
        if is_float(total_balance):
            data['total_balance'] = total_balance
            break
        else:
            print("Please input an integer or float")


    while sent == True:
        for c in range(1, len(categories)):
            if categories[c] == 'other':
                data['other'] = int(data['total_balance']) - check
                sent = False
                break 
            while True:
                expense = input("Enter expense for " + categories[c] + ": ")
                if is_float(expense):
                    data[categories[c]] = int(expense)
                    check += int(expense)
                    break
                else:
                    print("Error entering value")
            if check > int(data['total_balance']):
                print("Your budgeting exceeded the total budget, please re-enter all the values again")
                check = 0
                break   
    with open("info.json", "w") as file:
        json.dump(data, file)


def write_data(request_data, json_data):
    sent = True
    check = 0
    categories = ['total_balance', 'food', 'house_hold', 'clothing', 
                'personal_expense', 'subscription',
                'housing_expense', 'insurance', 'other']

    while True:
        total_balance = request_data.get("total_balance")
        if is_float(total_balance):
            json_data['total_balance'] = float(total_balance)
            break
        else:
            print("Please input an integer or float")

    while sent:
        for c in range(1, len(categories)):
            if categories[c] == 'other':
                json_data['other'] = float(json_data['total_balance']) - check
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
                "total_balance":0, "food":0, "house_hold":0, "clothing":0,
                "personal_expense":0, "subscription":0,"housing_expense":0,
                "insurance":0,"other":0}, file)
        

# A function which return's the dictionary/hashmap within the file          
def get_data():
    with open('info.json', 'r') as file:
        data = json.load(file)
        return data



if __name__ == "__main__":
    app.run(debug=True)