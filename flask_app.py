from flask import Flask, render_template, session, redirect,request
from flask_bootstrap import Bootstrap
from property_notifier import *
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField
from wtforms.validators import DataRequired

app=Flask(__name__)
bootstrap=Bootstrap(app)
app.config['SECRET_KEY']='X10FRET14'

class InitialForm(FlaskForm):
    user_type=SelectField('What brings you here today?',choices=[('Renter','I am looking for properties to rent'),
    ('Owner Occupier','I am looking for properties to purchase as a primary residence'),
    ('Investor', 'I am looking for properties to purchase for investment purposes')])
    next=SubmitField('Next')

@app.route('/initial_page',methods=['GET','POST'])
def initial_page():
    initial_form=InitialForm()
    if request.method == 'POST':
        if initial_form.validate_on_submit:
            if request.form['user_type']=='Renter':
                return redirect('/renter')
            elif request.form['user_type']=='Owner Occupier':
                return redirect('/owner_occupier')
            elif request.form['user_type']=='Investor':
                return redirect('/investor')
    
    return render_template('initial_page.html',form=initial_form)

@app.route('/renter',methods=['GET','POST'])
def renter():
    return render_template('renter.html')

@app.route('/owner_occupier',methods=['GET','POST'])
def owner_occupier():
    return render_template('owner_occupier.html')

@app.route('/investor',methods=['GET','POST'])
def investor():
    return render_template('investor.html')
