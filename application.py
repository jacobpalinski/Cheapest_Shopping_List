import regex as re
from decimal import ROUND_DOWN
from flask import Flask, render_template, session, redirect,request, flash, url_for
from flask_bootstrap import Bootstrap
from property_notifier import *
from custom_validators import *
from flask_wtf import FlaskForm
from wtforms import SelectField,SubmitField, TextAreaField, SelectMultipleField, DateField, DecimalField, EmailField, PasswordField
from wtforms.validators import InputRequired, DataRequired, NumberRange, Email

application=Flask(__name__,static_folder = 'static')
bootstrap=Bootstrap(application)
application.config['SECRET_KEY']='X10FRET14'

class InitialForm(FlaskForm):
    user_type=SelectField('What brings you here today?',choices=[('Renter','I am looking for properties to rent'),
    ('Owner Occupier','I am looking for properties to purchase as a primary residence'),
    ('Investor', 'I am looking for properties to purchase for investment purposes')],
    validators=[DataRequired('Please select an option')])
    email=EmailField('Email',validators=[email_from_options,Email('Please enter a valid email address',check_deliverability=True)])
    password=PasswordField('Password',validators=[EmailPassword('email')])
    next=SubmitField('Next')
        
class RenterForm(FlaskForm):
    locations=TextAreaField('What suburbs are you interested in?',
    validators = [InputRequired('Please input suburbs'),
    location_validation])
    property_types=SelectMultipleField('What kinds of properties are you interested in? Select all that apply',
    choices=[('House','House'),('ApartmentUnitFlat','Apartment'),('Townhouse','Townhouse')],
    validators=[DataRequired('Please select at least one option')])
    bedrooms=SelectField('How many bedrooms?',choices=[(1,1),(2,2),(3,3),(4,4),(5,5)],validators= 
    [DataRequired('Please select an option')])
    bathrooms=SelectField('How many bathrooms?',choices=[(1,1),(2,2),(3,3),(4,4),(5,5)],validators= 
    [DataRequired('Please select an option')])
    car_spaces=SelectField('How many carspaces?',choices=[(1,1),(2,2),(3,3),(4,4),(5,5)],validators= 
    [DataRequired('Please select an option')])
    date_posted=DateField('Earliest Posting Date',format='%Y-%m-%d',validators=
    [DataRequired('Please enter date in the DD-MM-YYYY format')])
    max_price=DecimalField('Enter maximum price you are willing to pay',places=0,rounding=ROUND_DOWN,validators=[
    InputRequired('Please enter price >0'),NumberRange(min=0,message='Please enter price >0')])
    min_price=DecimalField('Enter minimum price you are willing to pay',places=0,rounding=ROUND_DOWN,validators=
    [InputRequired('Please enter price >0'),MaxPriceLessThanMinPrice('max_price','Minimum price must be less than maximum price'),
    NumberRange(min=0,message='Please enter price >0')])

class InvestorForm(RenterForm):
    loan_type=SelectField('Do you wish to take a Fixed or Variable Rate Loan?',choices=[('Fixed','Fixed'),
    ('Variable','Variable')],validators=[DataRequired('Please select at least one option')])
    variable_loan_type=SelectField('Principal and Interest or Interest Only Variable Loan? (If Fixed select None)',
    choices=[('None','None'),('Interest Only','Interest Only'),
    ('Principal and Interest','Principal and Interest')],
    validators=[DataRequired('Please select at least one option'),CheckValidVariableLoanType('loan_type')])
    lvr=DecimalField('Enter LVR of home loan',places=0,rounding=ROUND_DOWN,
    validators=[InputRequired('Please enter an LVR'),NumberRange(min=0,max=100,message='Please enter an LVR between 0-100')])
    loan_term=DecimalField('Enter loan term',places=0,rounding=ROUND_DOWN,validators=[InputRequired('Please enter loan term'),
    ValidLoanTerm('variable_loan_type')])

class OwnerOccupierForm(InvestorForm):
    pass

RenterForm.next=SubmitField('Submit')

@application.route('/')
def default():
    return redirect(url_for('initial_page'))

@application.route('/initial_page',methods=['GET','POST'])
def initial_page():
    initial_form=InitialForm()
    if request.method == 'POST':
        if initial_form.validate_on_submit():
            session['email']=initial_form.email.data
            session['password']=initial_form.password.data
            if request.form['user_type']=='Renter':
                return redirect('/renter')
            elif request.form['user_type']=='Owner Occupier':
                return redirect('/owneroccupier')
            elif request.form['user_type']=='Investor':
                return redirect('/investor')
    
    return render_template('initial_page.html',form=initial_form)

@application.route('/renter', methods=['GET', 'POST'])
def renter():
    renter = Renter()
    api_client = APIClient()
    api_client.generate_token()
    renter_form = RenterForm()
    if request.method == 'POST':
        if renter_form.validate_on_submit():
            for location in renter_form.locations.data.split('),'):
                location = location.replace('(', '').replace(')', '').strip(' ')
                location_elements = location.split(',')
                renter.locations.append(tuple(location_elements))
            renter.property_types = renter_form.property_types.data
            renter.bedrooms = int(renter_form.bedrooms.data)
            renter.bathrooms = int(renter_form.bathrooms.data)
            renter.car_spaces = int(renter_form.car_spaces.data)
            renter.date_posted = renter_form.date_posted.data.strftime('%Y-%m-%d')
            renter.max_price = int(renter_form.max_price.data)
            renter.min_price = int(renter_form.min_price.data)
            residential_listings_search = ResidentialListingsSearch(renter, api_client)
            residential_listings_search.listings_request()
            property_data = PropertyData(residential_listings_search)
            property_data.common_listings_data()
            if len(property_data.data) == 0:
                flash(f'There are no {renter.bedrooms} bedroom, {renter.bathrooms} bathroom, {renter.car_spaces} car space {",".join(str.lower(property_type)+"s" for property_type in renter.property_types)} in {",".join({location[0] for location in renter.locations})}, with weekly rents between ${renter.min_price} and ${renter.max_price}, earliest posting date {renter.date_posted}. Please adjust form inputs')
                return render_template('renter.html',form = renter_form)
            property_data.listings_data_rent()
            customer_email = CustomerEmail(property_data = property_data, email_address = session.get('email'), password = session.get('password'))
            customer_email.create_csv_attachment()
            if re.search(r'@.+',customer_email.email_address).group(0) == '@gmail.com':
                customer_email.send_email_renter(customer_email.smtp_servers.get('Gmail'))
            elif re.search(r'@.+',customer_email.email_address).group(0) in ['@outlook.com', '@hotmail.com', '@live.com', '@msn.com']:
                customer_email.send_email_renter(customer_email.smtp_servers.get('Microsoft'))
            property_data.data.clear()
            return redirect('/thankyou')
    
    return render_template('renter.html',form = renter_form)

@application.route('/investor',methods=['GET','POST'])
def investor():
    investor = Investor()
    api_client = APIClient()
    api_client.generate_token()
    investor_form = InvestorForm()
    if request.method == 'POST':
        if investor_form.validate_on_submit():
            for location in investor_form.locations.data.split('),'):
                location = location.replace('(', '').replace(')', '').strip(' ')
                location_elements = location.split(',')
                investor.locations.append(tuple(location_elements))
            investor.property_types = investor_form.property_types.data
            investor.bedrooms = int(investor_form.bedrooms.data)
            investor.bathrooms = int(investor_form.bathrooms.data)
            investor.car_spaces = int(investor_form.car_spaces.data)
            investor.date_posted = investor_form.date_posted.data.strftime('%Y-%m-%d')
            investor.max_price = int(investor_form.max_price.data)
            investor.min_price = int(investor_form.min_price.data)
            investor.loan_type = investor_form.loan_type.data
            investor.variable_loan_type = investor_form.variable_loan_type.data
            investor.lvr = int(investor_form.lvr.data)
            investor.loan_term = int(investor_form.loan_term.data)
            if investor.loan_type == 'Fixed':
                investor.fixed_loan_rate(investor_rate_information)
            elif investor.loan_type == 'Variable':
                investor.variable_loan_rate(investor_rate_information)
            residential_listings_search = ResidentialListingsSearch(investor, api_client)
            residential_listings_search.listings_request()
            property_data = PropertyData(residential_listings_search)
            property_data.common_listings_data()
            if len(property_data.data) == 0:
                flash(f'There are no {investor.bedrooms} bedroom, {investor.bathrooms} bathroom, {investor.car_spaces} car space {",".join(property_type+"s" for property_type in investor.property_types)} in {",".join({location[0] for location in investor.locations})}, priced between ${investor.min_price} and ${investor.max_price}, earliest posting date {investor.date_posted}. Please adjust form inputs')
                return render_template('investor.html',form = investor_form)
            property_data.listings_data_sale()
            suburb_performance_statistics = SuburbPerformanceStatistics(investor, api_client, property_data)
            for index in range(len(suburb_performance_statistics.data)):
                if suburb_performance_statistics.data[index]['Property Type'] != 'ApartmentUnitFlat': # Meaning either house or townhouse 
                    if not suburb_performance_statistics.api_calls_made.get(('House', suburb_performance_statistics.data[index]['Suburb'],suburb_performance_statistics.data[index]['State'],suburb_performance_statistics.data[index]['Postcode'])):
                        suburb_performance_statistics.house_statistics(index)
                    suburb_performance_statistics.calculate_investor_metrics(index, 'House')
                elif suburb_performance_statistics.data[index]['Property Type'] == 'ApartmentUnitFlat':
                    if not suburb_performance_statistics.api_calls_made.get(('Apartment',suburb_performance_statistics.data[index]['Suburb'],suburb_performance_statistics.data[index]['State'],suburb_performance_statistics.data[index]['Postcode'])):
                        suburb_performance_statistics.apartment_statistics(index)
                    suburb_performance_statistics.calculate_investor_metrics(index, 'Apartment')
            customer_email = CustomerEmail(suburb_performance_statistics = suburb_performance_statistics, email_address = session.get('email'), password = session.get('password'))
            customer_email.create_csv_attachment()
            if re.search(r'@.+', customer_email.email_address).group(0) == '@gmail.com':
                customer_email.send_email_investor_owner_occupier(customer_email.smtp_servers.get('Gmail'))
            elif re.search(r'@.+', customer_email.email_address).group(0) in ['@outlook.com', '@hotmail.com', '@live.com', '@msn.com']:
                customer_email.send_email_investor_owner_occupier(customer_email.smtp_servers.get('Microsoft'))
            suburb_performance_statistics.data.clear()
            property_data.data.clear()
            return redirect('/thankyou')
                
    return render_template('investor.html',form=investor_form)

@application.route('/owneroccupier',methods=['GET','POST'])
def owner_occupier():
    owner_occupier = OwnerOccupier()
    api_client = APIClient()
    api_client.generate_token()
    owner_occupier_form = OwnerOccupierForm()
    if request.method == 'POST':
        if owner_occupier_form.validate_on_submit():
            for location in owner_occupier_form.locations.data.split('),'):
                location = location.replace('(', '').replace(')', '').strip(' ')
                location_elements = location.split(',')
                owner_occupier.locations.append(tuple(location_elements))
            owner_occupier.property_types = owner_occupier_form.property_types.data
            owner_occupier.bedrooms = int(owner_occupier_form.bedrooms.data)
            owner_occupier.bathrooms = int(owner_occupier_form.bathrooms.data)
            owner_occupier.car_spaces = int(owner_occupier_form.car_spaces.data)
            owner_occupier.date_posted = owner_occupier_form.date_posted.data.strftime('%Y-%m-%d')
            owner_occupier.max_price = int(owner_occupier_form.max_price.data)
            owner_occupier.min_price = int(owner_occupier_form.min_price.data)
            owner_occupier.loan_type = owner_occupier_form.loan_type.data
            owner_occupier.variable_loan_type = owner_occupier_form.variable_loan_type.data
            owner_occupier.lvr = int(owner_occupier_form.lvr.data)
            owner_occupier.loan_term = int(owner_occupier_form.loan_term.data)
            if owner_occupier.loan_type =='Fixed':
                owner_occupier.fixed_loan_rate(owner_occupier_rate_information)
            elif owner_occupier.loan_type == 'Variable':
                owner_occupier.variable_loan_rate(owner_occupier_rate_information)
            residential_listings_search = ResidentialListingsSearch(owner_occupier, api_client)
            residential_listings_search.listings_request()
            property_data = PropertyData(residential_listings_search)
            property_data.common_listings_data()
            if len(property_data.data) == 0:
                flash(f'There are no {owner_occupier.bedrooms} bedroom, {owner_occupier.bathrooms} bathroom, {owner_occupier.car_spaces} car space {",".join(property_type + "s" for property_type in owner_occupier.property_types)} in {",".join({location[0] for location in owner_occupier.locations})}, priced between ${owner_occupier.min_price} and ${owner_occupier.max_price}, earliest posting date {owner_occupier.date_posted}. Please adjust form inputs')
                return render_template('owner_occupier.html',form=owner_occupier_form)
            property_data.listings_data_sale()
            suburb_performance_statistics = SuburbPerformanceStatistics(owner_occupier, api_client, property_data)
            for index in range(len(suburb_performance_statistics.data)):
                if suburb_performance_statistics.data[index]['Property Type'] != 'ApartmentUnitFlat': # Meaning either house or townhouse
                    if not suburb_performance_statistics.api_calls_made.get(('House', suburb_performance_statistics.data[index]['Suburb'], suburb_performance_statistics.data[index]['State'], suburb_performance_statistics.data[index]['Postcode'])):
                        suburb_performance_statistics.house_statistics(index)
                    suburb_performance_statistics.calculate_owner_occupier_metrics(index, 'House')
                elif suburb_performance_statistics.data[index]['Property Type'] == 'ApartmentUnitFlat':
                    if not suburb_performance_statistics.api_calls_made.get(('Apartment', suburb_performance_statistics.data[index]['Suburb'], suburb_performance_statistics.data[index]['State'], suburb_performance_statistics.data[index]['Postcode'])):
                        suburb_performance_statistics.apartment_statistics(index)
                    suburb_performance_statistics.calculate_owner_occupier_metrics(index, 'Apartment')
            customer_email = CustomerEmail(suburb_performance_statistics = suburb_performance_statistics, email_address = session.get('email'), password = session.get('password'))
            customer_email.create_csv_attachment()
            if re.search(r'@.+', customer_email.email_address).group(0) == '@gmail.com':
                customer_email.send_email_investor_owner_occupier(customer_email.smtp_servers.get('Gmail'))
            elif re.search(r'@.+', customer_email.email_address).group(0) in ['@outlook.com', '@hotmail.com', '@live.com', '@msn.com']:
                customer_email.send_email_investor_owner_occupier(customer_email.smtp_servers.get('Microsoft'))
            suburb_performance_statistics.data.clear()
            property_data.data.clear()
            return redirect('/thankyou')
        
    return render_template('owner_occupier.html',form=owner_occupier_form)

@application.route('/thankyou',methods=['GET'])
def thankyou():
    return render_template('thankyou.html')

if __name__=="__main__":
    application.run(port=5000)
