import pytest
import pytest_mock
from application import app
from flask import request
from property_notifier import *
import datetime
from decimal import Decimal

@pytest.fixture
def client():
    app.config['TESTING']=True
    app.config['WTF_CSRF_ENABLED']=False
    return app.test_client()

class Test_Initial_Page:
    
    def test_initial_page_get(self,client):
        resp=client.get('/initial_page')
        assert resp.status_code == 200
        assert b'<title>Domain Property Notifier</title>' in resp.data
        assert b'<h1>Domain Property Notifier</h1>' in resp.data
        assert b'<p>Generate email notifications for the properties you want to rent, own or invest in as listed on Domain.com.au.\n    Your email body will contain property information based on intended purpose and criterea provided, \n    including a CSV file for download. Select an appropriate option from the question below, enter Gmail or \n    Microsoft account email and password (in-app password for Gmail) and click next to get started.</p>' in resp.data
        assert b'class="form"' in resp.data # checks InitialForm included in response

    def test_initial_page_post_user_type_Renter_app_specific_password(self,client):
        resp=client.post('/initial_page',data={'user_type':'Renter','email':'kpalinski99@gmail.com',
        'password':'viemyqimzeyoaebc'})
        assert resp.status_code == 302
        assert b'href="/renter"' in resp.data

    def test_initial_page_post_user_type_Renter_gmail_account_password(self,client):
        resp=client.post('/initial_page',data={'user_type':'Renter','email':'kpalinski99@gmail.com',
        'password':'Buleczka4'})
        assert resp.status_code == 200
    
    def test_initial_page_post_user_type_Renter_gmail_wrong_password(self,client):
        resp=client.post('/initial_page',data={'user_type':'Renter','email':'kpalinski99@gmail.com',
        'password':'wrongpassword'})
        assert resp.status_code==200
    
    def test_initial_page_post_user_type_Renter_outlook_account_password(self,client):
        resp=client.post('/initial_page',data={'user_type':'Renter','email':'jacob.palinski@outlook.com',
        'password':'Workjob91$'})
        assert resp.status_code==302
        assert b'href="/renter"' in resp.data
    
    def test_initial_page_post_user_type_Renter_outlook_wrong_password(self,client):
        resp=client.post('/initial_page',data={'user_type':'Renter','email':'jacob.palinski@outlook.com',
        'password':'wrongpassword'})
        assert resp.status_code==200

    def test_initial_page_post_user_type_Owner_Occupier_outlook_account_password(self,client):
        resp=client.post('/initial_page',data={'user_type':'Owner Occupier','email':'jacob.palinski@outlook.com',
        'password':'Workjob91$'})
        assert resp.status_code == 302
        assert b'href="/owner_occupier"' in resp.data

    def test_initial_page_post_user_type_Investor_outlook_account_password(self,client):
        resp=client.post('/initial_page',data={'user_type':'Investor','email':'jacob.palinski@outlook.com',
        'password':'Workjob91$'})
        assert resp.status_code == 302
        assert b'href="/investor"' in resp.data

class Test_Renter_Page:
    def test_renter_page_get(self,client):
        resp=client.get('/renter')
        assert resp.status_code == 200
        assert b'<title>Renter Information</title>' in resp.data
        assert b'<h1>Rental Property Information Form</h1>' in resp.data
        assert b'<p>Fill out the below form and a CSV containing Listing Date, Property Type, Suburb, State, Postcode,\n    Property Address, Weekly Rent, Annual Rent, Land Area (if applicable) and URL will be sent to your email address.</p>' in resp.data
        assert b'class="form"' in resp.data # checks Renter_Form included in response
    
    def test_renter_post_all_validators_true(self,client):
        resp=client.post('/renter',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400')})
        assert resp.status_code == 302
    
    def test_renter_post_validator_fail_suburbs_comma_seperated_with_whitespace(self,client):
        resp=client.post('/renter',data={'suburbs': 'Madeley, Applecross, Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400')})
        assert resp.status_code == 200

    def test_renter_post_validator_fail_suburbs_invalid_suburb(self,client):
        resp=client.post('/renter',data={'suburbs': 'Madeley,Applecross,Narnia',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400')})
        assert resp.status_code == 200

    def test_renter_post_validator_fail_property_types_no_selection(self,client):
        resp=client.post('/renter',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': [],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400')})
        assert resp.status_code == 200
    
    def test_renter_post_validator_fail_date_posted(self,client):
        resp=client.post('/renter',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': None,
        'max_price': Decimal('500'),
        'min_price': Decimal('400')})
        assert resp.status_code == 200
    
    @pytest.mark.parametrize('price',[Decimal('-200'),Decimal('200')])
    def test_renter_post_max_price_validator_fail_numbers(self,price,client):
        resp=client.post('/renter',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': price,
        'min_price': Decimal('400')})
        assert resp.status_code == 200
    
    def test_renter_post_max_price_validator_fail_none(self,client):
        with pytest.raises(TypeError) as excinfo:
            resp=client.post('/renter',data={'suburbs': 'Madeley,Applecross,Darch',
            'property_types': ['House','Townhouse'],
            'bedrooms': '2',
            'bathrooms': '2',
            'car_spaces': '2',
            'date_posted': datetime.date(2022,8,25),
            'max_price': None,
            'min_price': Decimal('400')})
        assert "'>=' not supported between instances of 'decimal.Decimal' and 'NoneType'" in str(excinfo.value)
    
    @pytest.mark.parametrize('price',[None,Decimal('-200'),Decimal(600)])
    def test_renter_post_min_price_validator_fail(self,price,client):
        resp=client.post('/renter',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': price})
        assert resp.status_code==200

class Test_Investor_Page:
    def test_investor_page_get(self,client):
        resp=client.get('/investor')
        assert resp.status_code == 200
        assert b'<title>Investor Information</title>' in resp.data
        assert b'<h1>Investor Property Information Form</h1>' in resp.data
        assert b'<p>Fill out the below form and a CSV containing Listing Date, Property Address, Property Type, Suburb, State, Postcode, Price,\n    Land Area (if applicable), URL, Mortgage Repayments, Rental Income, Operating Expenses, Cash Flow, Cash on Cash Return,\n    1yr Appreciation, 5yr Appreciation and 10yr Appreciation will be sent to your email address.</p>' in resp.data
        assert b'<p><b><u>Valid Loan Terms</u></b></p>' in resp.data
        assert b'<p><b>Fixed Rate Loan</b>: 1-5 years</p>' in resp.data
        assert b'<p><b>Variable Rate Loan Interest Only</b>: 5-10 years</p>' in resp.data
        assert b'<p><b>Variable Rate Loan Principal and Interest</b>: 10,15,20,25 or 30 years</p>' in resp.data
        assert b'class="form"' in resp.data # checks InvestorForm included in response
    
    # suburbs, property_types, bedrooms, bathrooms, car_spaces, date_posted, max_price, min_price not tested due to inheritance from RenterForm

    @pytest.mark.parametrize('variable_loan_type',['Interest Only','Principal and Interest'])
    def test_investor_post_CheckValidVariableLoanType_validator_fail_fixed_rate(self,variable_loan_type,client):
        resp=client.post('/investor',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400'),
        'loan_type': 'Fixed',
        'variable_loan_type': variable_loan_type,
        'lvr': Decimal('80'),
        'loan_term': Decimal('2')})
        assert resp.status_code==200
    
    def test_investor_post_CheckValidVariableLoanType_validator_fail_variable_rate(self,client):
        resp=client.post('/investor',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400'),
        'loan_type': 'Variable',
        'variable_loan_type': 'None',
        'lvr': Decimal('80'),
        'loan_term': Decimal('2')})
        assert resp.status_code==200
    
    def test_investor_post_lvr_InputRequired_validator_fail(self,client):
        resp=client.post('/investor',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400'),
        'loan_type': 'Fixed',
        'variable_loan_type': 'None',
        'lvr': None,
        'loan_term': Decimal('2')})
        assert resp.status_code==200

    @pytest.mark.parametrize('lvr_input',[Decimal('-1'),Decimal('101')])
    def test_investor_post_lvr_NumberRange_validator_fail(self,lvr_input,client):
        resp=client.post('/investor',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400'),
        'loan_type': 'Fixed',
        'variable_loan_type': 'None',
        'lvr': lvr_input,
        'loan_term': Decimal('2')})
        assert resp.status_code==200
    
    def test_investor_post_loan_term_InputRequired_validator_fail(self,client):
        resp=client.post('/investor',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400'),
        'loan_type': 'Fixed',
        'variable_loan_type': 'None',
        'lvr': Decimal('80'),
        'loan_term': None})
        assert resp.status_code==200

    @pytest.mark.parametrize('loan_term',[Decimal('0'),Decimal('6')])
    def test_investor_post_loan_term_ValidLoanTerm_validator_fail_fixed_rate(self,loan_term,client):
        resp=client.post('/investor',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400'),
        'loan_type': 'Fixed',
        'variable_loan_type': 'None',
        'lvr': Decimal('80'),
        'loan_term': loan_term})
        assert resp.status_code==200
    
    @pytest.mark.parametrize('loan_term',[Decimal('4'),Decimal('11')])
    def test_investor_post_loan_term_ValidLoanTerm_validator_fail_variable_rate_interest_only(self,loan_term,client):
        resp=client.post('/investor',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400'),
        'loan_type': 'Variable',
        'variable_loan_type': 'Interest Only',
        'lvr': Decimal('80'),
        'loan_term': loan_term})
        assert resp.status_code==200
    
    @pytest.mark.parametrize('loan_term',[Decimal('9'),Decimal('11'),Decimal('16'),Decimal('21'),Decimal('26'),Decimal('31')])
    def test_investor_post_loan_term_ValidLoanTerm_validator_fail_variable_rate_principal_and_interest(self,loan_term,client):
        resp=client.post('/investor',data={'suburbs': 'Madeley,Applecross,Darch',
        'property_types': ['House','Townhouse'],
        'bedrooms': '2',
        'bathrooms': '2',
        'car_spaces': '2',
        'date_posted': datetime.date(2022,8,25),
        'max_price': Decimal('500'),
        'min_price': Decimal('400'),
        'loan_type': 'Variable',
        'variable_loan_type': 'Principal and Interest',
        'lvr': Decimal('80'),
        'loan_term': loan_term})
        assert resp.status_code==200
    
class Test_Owner_Occupier_Page:
    def test_owner_occupier_page_get(self,client):
        resp=client.get('/owner_occupier')
        assert resp.status_code == 200
        assert b'<title>Owner Occupier Information</title>' in resp.data
        assert b'<h1>Owner Occupier Property Information Form</h1>' in resp.data
        assert b'<p>Fill out the below form and a CSV containing Listing Date, Property Address, Property Type, Suburb, State, Postcode, Price,\n    Land Area (if applicable), URL, Mortgage Repayments and 10yr Appreciation will be sent to your email address.</p>' in resp.data
        assert b'<p><b><u>Valid Loan Terms</u></b></p>' in resp.data
        assert b'<p><b>Fixed Rate Loan</b>: 1-5 years</p>' in resp.data
        assert b'<p><b>Variable Rate Loan Interest Only</b>: 5-10 years</p>' in resp.data
        assert b'<p><b>Variable Rate Loan Principal and Interest</b>: 10,15,20,25 or 30 years</p>' in resp.data
        assert b'class="form"' in resp.data # checks InvestorForm included in response

    # No tests for owner_occupier inputs as it inherits all the same form fields as the investor class, therefore tests would be redundant.

