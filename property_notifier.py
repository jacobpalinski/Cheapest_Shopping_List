import requests

class User:
    def __init__(self):
        self.user_type=None
        self.suburbs=[]
        self.property_types=[]
        self.min_price=None
        self.max_price=None
        self.bedrooms=None
        self.bathrooms=None
        self.area=None
        self.date_posted=None #earliest date posting when searching for property
        self.car_spaces=None
        self.target_appreciation=None
        self.target_rentalyield=None
    
    def prompt(self):
        
        self.user_type=input('Are you a investor, home buyer or a renter? Enter One ').lower().title()

        num_suburbs=int(input('How many suburbs are you interested in? '))
        self.suburbs.extend(input(f'Please enter the {num_suburbs} you are interested in: ').lower().title().replace('And',',').split(','))
        
        self.property_types=input('Which of the following are you interested in: Houses, Apartments, Townhouses? ').lower().title().replace('And',',').replace(' ','').split(',')
        self.min_price=int(input('Enter minimum price you are willing to pay for property ($AUD): ').strip(','))
        self.max_price=int(input('Enter maximum price you are willing to pay for property ($AUD): ').strip(','))
        self.bedrooms=int(input('Enter number of bedrooms '))
        self.bathrooms=int(input('Enter number of bathrooms '))
        
        if 'Houses' in self.property_types:
            self.area=int(input('Please enter minimum desired Land Area (sqm): ')) #on domain search only land area for houses is shown

        self.date_posted=input('Latest posting date (yyyy-mm-dd)? ')
        self.car_spaces=int(input('How many car spaces? Enter Number '))

        if self.user_type in ['Home Buyer', 'Investor']:
            self.target_appreciation=float(input('What is your desired appreciation on the property (%)? '))
            self.target_rentalyield=float(input('What is your desired rental yield on the property (%)? '))

class API:
    def __init__(self):
        self.url=' https://auth.domain.com.au/v1/connect/token'
        self.client_id='client_4233d25eceb0e463018f9c809e1f43a8'
        self.client_secret='secret_597027cbb4d6b1a839794fc6b71decb9'
        self.scopes=['api_listings_read api_suburbperformance_read']
    
    def generate_token(self):
        auth_response=requests.post(self.url,{
            'client_id':self.client_id,
            'client_secret':self.client_secret,
            'grant_type':'client_credentials',
            'scope':self.scopes,
            'Content-Type':'text/json'
        })
        json_response=auth_response.json()
        self.access_token=json_response['access_token']

class Property_Data:
    def __init__(self):
        self.property_list=[]
    
    def listings_search(self):
        pass

    def listings_info(self):
        pass

    def statistics(self):
        pass


class customer_email:

    def __init__(self):
        self.username=None
        self.password=None
    
    def prompt(self):
        pass

    def email_body(self):
        pass

    def send_email(self):
        pass




