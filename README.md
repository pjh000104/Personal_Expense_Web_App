# Personal Expense Web Application

This is a Flask-based web application for managing personal expenses. The application allows users to register, log in, manage balances for different categories, and play a built-in Snake game for entertainment. It integrates Flask-SQLAlchemy for database management and Flask-Migrate for database migrations.

## Features

- **User Authentication**: 
  - Registration and login functionality.
  - Secure session management using `Flask` sessions.

- **Expense Management**:
  - Initialize and update balances for categories such as food, clothing, subscriptions, and more.
  - Track remaining balances for each category.
  - Manage expenses dynamically using JSON and SQLAlchemy.

- **Interactive Game**:
  - A built-in Snake game implemented with `pygame`.

- **Database Integration**:
  - SQLite backend for persistent data storage.
  - SQLAlchemy ORM for database operations.

## Project Structure

```
Personal_Expense_Web_App/
├── __pycache__/
├── css/
├── instance/
├── migrations/
├── static/
│   ├── css/
│   ├── images/
│   ├── js/
├── templates/
│   ├── about.html
│   ├── register.html
│   ├── login.html
│   ├── main.html
│   ├── spendBalance.html
│   ├── checkBalance.html
├── app.py
├── info.json
├── models.py
```

## Database Models

### User Model

Represents the users of the application.

| Field        | Type         | Description                  |
|--------------|--------------|------------------------------|
| `id`         | Integer      | Primary Key                 |
| `name`       | String(80)   | User's name                 |
| `email`      | String(120)  | Unique user email           |
| `password`   | String(120)  | User's password             |
| `expenses`   | Relationship | Relationship to `Expense`   |

### Expense Model

Tracks expenses for individual users.

| Field              | Type         | Default Value |
|--------------------|--------------|---------------|
| `id`              | Integer      | Primary Key   |
| `user_id`         | Integer      | Foreign Key   |
| `total_balance`   | Float        | 0             |
| `food`            | Float        | 0             |
| `house_hold`      | Float        | 0             |
| `clothing`        | Float        | 0             |
| `personal_expense`| Float        | 0             |
| `subscription`    | Float        | 0             |
| `housing_expense` | Float        | 0             |
| `insurance`       | Float        | 0             |
| `other`           | Float        | 0             |

## Routes

| Route                   | Methods     | Description                                      |
|-------------------------|-------------|--------------------------------------------------|
| `/register`             | GET, POST   | User registration.                              |
| `/login`                | GET, POST   | User login.                                     |
| `/add_balance`          | GET, POST   | Add a balance to initialize categories.         |
| `/initialize_balance`   | GET, POST   | Initializes balance categories for the user.    |
| `/spend_balance`        | GET         | View and manage category balances.              |
| `/spend/<category>`     | GET, POST   | Spend money from a specific category.           |
| `/checkBalance`         | GET         | Check balance details for all categories.       |
| `/snake_game`           | GET         | Launch the Snake game.                          |
| `/check_balances`       | GET         | View all balances for the current user.         |

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Pygame

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/pjh000104/Personal_Expense_Web_App.git
   cd Personal_Expense_Web_App
2, Install dependencies:
```bash
pip install -r requirements.txt
```
3, Initialize the database:
```
flask db init
flask db migrate
flask db upgrade
```
4, Run the application 
```
Run the application:
```
5, Access the application at http://127.0.0.1:5000.

## Usage

- Register a new account.
- Log in with your credentials.
- Add balances to initialize budget categories.
- Manage expenses by adding or spending within categories.
- Check your balances at any time.
- Play the Snake game for a break!
