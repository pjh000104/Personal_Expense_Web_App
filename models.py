from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_balance = db.Column(db.Float, default=0)
    food = db.Column(db.Float, default=0)
    house_hold = db.Column(db.Float, default=0)
    clothing = db.Column(db.Float, default=0)
    personal_expense = db.Column(db.Float, default=0)
    subscription = db.Column(db.Float, default=0)
    housing_expense = db.Column(db.Float, default=0)
    insurance = db.Column(db.Float, default=0)
    other = db.Column(db.Float, default=0)
