import binascii
import os

from flask import Flask, request, render_template, flash, redirect, url_for
from flask_restful import Resource, Api, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
import json, random

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.sqlite3_1'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
api = Api(app)

class Flight(db.Model):
    id = db.Column('flight_id', db.Integer, unique=True, primary_key=True, autoincrement=True)
    fromCity=db.Column(db.String(80))
    toCity =db.Column(db.String(80))
    deptTime = db.Column(db.String(80))
    arrivalTime = db.Column(db.String(80))
    airplane = db.Column(db.String(80))
    passNumber = db.Column(db.Integer)


    def __init__(self, fromCity, toCity, depTime, arrivalTime, airplane, passNumber):
        self.fromCity=fromCity
        self.toCity=toCity
        self.deptTime=depTime
        self.arrivalTime = arrivalTime
        self.airplane=airplane
        self.passNumber=passNumber

authenticated = False
@app.route('/authentication_authorization/', methods=['GET', 'POST'])
def login():
    global authenticated
    if request.method == 'POST':
        ausername = request.form['username']
        apass = request.form['password']
        f = open('admins.json')
        admins = json.load(f)
        f.close()
        for admin in admins['admins']:
            if admin['username']==ausername:
                if admin['password']==apass:
                    atoken = generate_key()
                    authenticated = True
                    flash('Admin logged in successfully!')
                    break
                else:
                    print('Invalid password!')
        if authenticated == False:
            print('Your user is not an admin!')
        return redirect(url_for('show_all'))
    return render_template('authentication.html')

def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()

@app.route('/flights/')
def show_all():
    return render_template('get_all.html', flights = Flight.query.all() )

@app.route('/flights/delete', methods=['GET','POST'])
def delete():
    if request.method =='POST':
        flight = Flight.query.filter_by(id = request.form['id']).first()
        db.session.delete(flight)
        db.session.commit()
        flash('Record successfully deleted')

        return redirect(url_for('show_all'))
    return render_template('delete.html')

@app.route('/flights/add', methods = ['GET', 'POST'])
def add():
    if request.method == "POST":
        if not request.form['fromCity'] or not request.form['toCity'] or not request.form['airplane'] or not request.form['deptTime']:
            flash('Please enter all the fields', 'error')
        else:
            flight = Flight(request.form['fromCity'], request.form['toCity'], request.form['deptTime'], request.form['arrivalTime'], request.form['airplane'], request.form['passNumber'])
            db.session.add(flight)
            db.session.commit()

            flash('record successfully added')
            return redirect(url_for('show_all'))
    return render_template('add.html')

@app.route('/flights/update', methods = ['GET', 'POST'])
def update():
    if request.method == "POST":
            flight = Flight.query.filter_by(id = request.form['id']).first()
            if request.form['fromCity']:
                flight.fromCity=request.form['fromCity']
            if request.form['toCity']:
                flight.toCity=request.form['toCity']
            if request.form['deptTime']:
                flight.deptTime=request.form['deptTime']
            if request.form['arrivalTime']:
                flight.arrivalTime = request.form['arrivalTime']
            if request.form['airplane']:
                flight.airplane = request.form['airplane']
            if request.form['passNumber']:
                flight.passNumber = request.form['passNumber']
            #    db.session.query.filter_by(id=request.form['id']).update({"passNumber":request.form['passNumber']})
            db.session.commit()

            flash('record successfully updated')
            return redirect(url_for('show_all'))
    return render_template('update.html')

if __name__ == "__main__":
    db.create_all()
    flight1 = Flight('Baku', 'Moscow', '12:12 10-01-2021', '15:30 10-01-2020', 'AZAL', 50)
    db.session.add(flight1)
    db.session.commit()
    app.run(debug=True)