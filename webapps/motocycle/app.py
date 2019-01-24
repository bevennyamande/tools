#!/usr/bin/env python

from flask import (Flask, render_template, request,
                  redirect, url_for, json, flash)
from flask_sqlalchemy import SQLAlchemy

# TODO: find a way to track usage of the application and traffic

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sjfkhsdfhskfhsf'
app.config['SQLQLCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
db = SQLAlchemy(app)

# Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80))
    # may change to phone number and use twilio api
    email = db.Column(db.String(80))
    date = db.Column(db.DateTime)

    vehicle = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    sold_by = db.relationship('Vehicle',
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, password, email):
        self.password = password
        self.email = email


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(80))
    picture = db.Column(db.String(70))
    description = db.Column(db.String(120))

    def __init__(self, details, description, picture=None):
        self.details = details
        self.picture = picture
        self.description = description


# routes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get search query
        # get length of returned results
        # get pagination
        query = request.form['query']
        total_results = 3
        return render_template('index.html', badge=total_results,
                               results=query)
    return render_template('index.html')


@app.route('/create_account', methods=['POST'])
def create_account():
    # check if password match client side using angularjs
    # research on how to send info to email and be linked back
    email = request.form['email']
    password = request.form['password']
    flash('Thank you, check email to confirm email address')
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if password and email:
        # check if they match
        return render_template('user.html')


@app.route('/authenticate/<token>')
def authenticate(token):
    pass

if __name__ == '__main__':
    app.run(debug=True)
