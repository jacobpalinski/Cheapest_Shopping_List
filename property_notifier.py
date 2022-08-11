import requests
import re

# keys in the form (loan type,lvr,loan term). Average per loan term for variable rates were not found so overall averages where used
# Variable-IO for owner occupier and investor where estimated using best available information
owner_occupier_rate_information={('fixed','=<80','=<3'):3.06,('fixed','=<80','>3'):3.84,('variable-PI','=<80'):2.46,
('variable-PI','>80'):2.81,('variable-IO','=<80'):3.19,('variable-IO','>80'):3.50}
investor_rate_information={('fixed','=<80','=<3'):3.34,('fixed','=<80','>3'):4.11,('variable-PI','=<80'):2.80,
('variable-PI','>80'):3.11,('variable-IO','=<80'):3.02,('variable-IO','>80'):3.35}

property_data=[]

class User:
    def __init__(self):
        self.locations=[] 
        self.property_types=[]
        self.bedrooms=None
        self.bathrooms=None
        self.date_posted=None # earliest date listing was posted
        self.car_spaces=None
        self.min_price=None # minimum of price range for home buyer/investor and rental range for renter
        self.max_price=None # maximum of price range for home buyer/investor and rental range for renter
    
    def prompt(self):
        suburbs=(input(f'Please enter the {num_suburbs} you are interested in: ').lower().title().replace('And',',').split(','))
        states=(input('Please enter the state of each suburb (NSW,VIC,ACT,WA,NT,TAS,QLD,SA): ').upper().replace(' ',',').replace('And,','').split(','))
        suburb_state=list(zip(suburbs,states)) # suburb,state combination as state is mandatory in listings_search call
        for suburbs,states in suburb_state:
            self.locations.append({f'{suburbs}':f'{states}'})

        self.property_types=input('Which of the following are you interested in: House, Apartment, Townhouse? ').lower().title().replace(' ',',').replace('And,','').replace('Apartment','ApartmentUnitFlat').split(',')
        self.bedrooms=int(input('Enter number of bedrooms: '))
        self.bathrooms=int(input('Enter number of bathrooms: '))
        self.car_spaces=int(input('Enter number of car spaces: '))
        self.date_posted=input('Latest posting date (yyyy-mm-dd)? ')
        self.min_price=int(input('What is the minimum for your price range? '))
        self.max_price=int(input('What is the maximum for your price range? '))
    
class Renter(User):
    pass

class Owner_Occupier(User):
    def __init__(self):
        super().__init__()
        self.loan_type=None
        self.variable_loan_type=None
        self.lvr=None
        self.loan_term=None
        self.mortgage_interest=None

    def prompt(self):
        super().prompt()
        self.loan_type=input('Variable or Fixed? Enter One: ').lower().title()
        if self.loan_type=='Variable':
            self.variable_loan_type=input('Enter interest only or principal and interest: ').lower().title()
            self.lvr=int(input('What is the LVR of the loan you are looking to take? '))
        elif self.loan_type=='Fixed':
            self.lvr=int(input('What is the LVR of the loan you are looking to take? Please enter value =<80: '))

    def fixed_loan_rate(self,owner_occupier_rate_information):
        self.loan_term=int(input('How many years do you want the loan for? Enter number between 1 and 5: '))
        if self.loan_term<=3:
            self.mortgage_interest=owner_occupier_rate_information[('fixed','=<80','=<3')]
        elif self.loan_term>3:
            self.mortgage_interest=owner_occupier_rate_information[('fixed','=<80','>3')]
    
    def variable_loan_rate(self,owner_occupier_rate_information):
        if self.variable_loan_type=='Principal And Interest':
            self.loan_term=int(input('How many years do you want the loan for? Enter 10,15,20,25 or 30: '))
            if self.lvr<=80:
                self.mortgage_interest=owner_occupier_rate_information[('variable-PI','=<80')]
            elif self.lvr>80:
                self.mortgage_interest=owner_occupier_rate_information[('variable-PI','>80')]

        elif self.variable_loan_type=='Interest Only':
            self.loan_term=int(input('How many years do you want the loan for? Enter number between 5 and 10: '))
            if self.lvr<=80:
                self.mortgage_interest=owner_occupier_rate_information[('variable-IO','=<80')]
            elif self.lvr>80:
                self.mortgage_interest=owner_occupier_rate_information[('variable-IO','>80')]

class Investor(Owner_Occupier,User):
    def __init__(self):
        super().__init__()
    
    def prompt(self):
        super().prompt()

    def fixed_loan_rate(self,investor_rate_information):
        self.loan_term=int(input('How many years do you want the loan for? Enter number between 1 and 5: '))
        if self.loan_term<=3:
            self.mortgage_interest=investor_rate_information[('fixed','=<80','=<3')]
        elif self.loan_term>3:
            self.mortgage_interest=investor_rate_information[('fixed','=<80','>3')]
    
    def variable_loan_rate(self,investor_rate_information):
        if self.variable_loan_type=='Principal And Interest':
            self.loan_term=int(input('How many years do you want the loan for? Enter 10,15,20,25 or 30: '))
            if self.lvr<=80:
                self.mortgage_interest=investor_rate_information[('variable-PI','=<80')]
            elif self.lvr>80:
                self.mortgage_interest=investor_rate_information[('variable-PI','>80')]

        elif self.variable_loan_type=='Interest Only':
            self.loan_term=int(input('How many years do you want the loan for? Enter number between 5 and 10: '))
            if self.lvr<=80:
                self.mortgage_interest=investor_rate_information[('variable-IO','=<80')]
            elif self.lvr>80:
                self.mortgage_interest=investor_rate_information[('variable-IO','>80')]

class API:
    def __init__(self):
        self.client_id='client_4233d25eceb0e463018f9c809e1f43a8'
        self.client_secret='secret_597027cbb4d6b1a839794fc6b71decb9'
        self.scopes=['api_listings_read api_suburbperformance_read']
    
    def generate_token(self):
        response=requests.post(f'https://auth.domain.com.au/v1/connect/token',{'client_id':self.client_id,
        'client_secret':self.client_secret, 'grant_type':'client_credentials','scope':self.scopes,
        'Content-Type':'text/json'})
        self.access_token={'Authorization':'Bearer '+ response.json()['access_token']}

class Residential_Listings_Search:
    def __init__(self):
        self.responses=[]
    
    def listings_request(self,user,api):
        for location in user.locations:
            for suburb,state in location.items():
                listings=requests.post('https://api.domain.com.au/v1/listings/residential/_search',json={
                    'listingType':'Rent' if isinstance(user,Renter) else 'Sale',
                    'propertyTypes':user.property_types,
                    'minBedrooms':user.bedrooms,
                    'minBathrooms':user.bathrooms,
                    'minCarspaces':user.car_spaces,
                    'minPrice':user.min_price,
                    'maxPrice':user.max_price,
                    'locations':[
                        {
                            'state': state,
                            'region': '',
                            'area': '',
                            'suburb':suburb,
                            'postcode': '',
                            'includeSurroundingSuburbs':False        
                        }
                    ],
                    'excludePriceWithheld': False,
                    'excludeDepositTaken': True,
                    'pageSize':50,
                    'listedSince':f'{user.date_posted}'}, headers=api.access_token)
                
                self.responses.append(listings.json())

def common_listings_data(user, property_data, residential_listings_search):
    for listings_json in residential_listings_search.responses:
        for properties in listings_json:
            if properties['type']=='PropertyListing':
                date_listing=re.search(r'[\d-]+',properties['listing']['dateListed']).group(0)
                type=properties['listing']['propertyDetails']['propertyType']
                suburb=properties['listing']['propertyDetails']['suburb'].lower().title()
                state=properties['listing']['propertyDetails']['state']
                postcode=properties['listing']['propertyDetails']['postcode']
                address=properties['listing']['propertyDetails']['displayableAddress']
                area=properties['listing']['propertyDetails']['landArea'] if properties['listing']['propertyDetails'].get('landArea') else 'N/A'
                display_price_search=re.search(r'(\d+(\.\d*)?)+',properties['listing']['priceDetails']['displayPrice'].replace(',',''))
                url='https://www.domain.com.au/' + properties['listing']['listingSlug']
                if display_price_search==None:
                    display_price=user.min_price
                else:
                    display_price=float(display_price_search.group(0))
                property_data.append({'Listing Date':date_listing,'Property Type':type,'Suburb': suburb,'State':state,
                'Postcode':postcode,'Address':address,'Land Area':area,'Price':display_price,'Url':url})
        
def listings_data_rent(property_data):
    for property in property_data:
        property['Weekly Rent']=property.pop('Price')
        property['Annual Rent']=(property['Weekly Rent']*52)

def listings_data_sale(property_data):
    for property in property_data:
        if property['Price']<100:
            property['Price']=property['Price']*1000000  # for display prices that contained millions symbol with number eg. 1.5M
        elif property['Price']<1000:
            property['Price']=property['Price']*1000 # for display prices that contained thousands symbol with number eg. 539K

class Suburb_Performance_Statistics:
    def __init__(self):
        self.api_calls_made={}
    
    def request_json(self,index,user,api,property_data,parameter):
        suburb_stats=requests.get('https://api.domain.com.au/v2/suburbPerformanceStatistics/' + property_data[index]['State'] + '/' 
        + property_data[index]['Suburb'].replace(' ','%20')+ '/' + property_data[index]['Postcode'] + '?' + f'propertyCategory={parameter}' 
        + '&' + f'bedrooms={user.bedrooms}'+ '&' + 'periodSize=years' + '&' + 'startingPeriodRelativeToCurrent=1' + '&' 
        + 'totalPeriods=11', headers=api.access_token)
        self.suburb_stats_json=suburb_stats.json()
    
    def house_statistics(self,index,user,api,property_data):
        self.request_json(index,user,api,property_data,'House')
        median_annual_rent=self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianRentListingPrice']
        median_sale_20212022=self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianSoldPrice']
        median_sale_20202021=self.suburb_stats_json['series']['seriesInfo'][9]['values']['medianSoldPrice']
        median_sale_20172018=self.suburb_stats_json['series']['seriesInfo'][5]['values']['medianSoldPrice']
        median_sale_20112012=self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianSoldPrice']
        appreciation_1yr=round(100.00*(median_sale_20212022-median_sale_20202021)/median_sale_20202021,2)
        appreciation_5yr=round(100.00*(median_sale_20212022-median_sale_20172018)/median_sale_20172018,2)
        appreciation_10yr=round(100.00*(median_sale_20212022-median_sale_20112012)/median_sale_20112012,2)
        self.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])]=[appreciation_1yr,
        appreciation_5yr,appreciation_10yr,median_annual_rent]
    
    def apartment_statistics(self,index,user,api,property_data):
        self.request_json(index,user,api,property_data,'Unit')
        median_annual_rent=self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianRentListingPrice']
        median_sale_20212022=self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianSoldPrice']
        median_sale_20202021=self.suburb_stats_json['series']['seriesInfo'][9]['values']['medianSoldPrice']
        median_sale_20172018=self.suburb_stats_json['series']['seriesInfo'][5]['values']['medianSoldPrice']
        median_sale_20112012=self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianSoldPrice']
        appreciation_1yr=round(100.00*(median_sale_20212022-median_sale_20202021)/median_sale_20202021,2)
        appreciation_5yr=round(100.00*(median_sale_20212022-median_sale_20172018)/median_sale_20172018,2)
        appreciation_10yr=round(100.00*(median_sale_20212022-median_sale_20112012)/median_sale_20112012,2)
        self.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])]=[appreciation_1yr,
        appreciation_5yr,appreciation_10yr,median_annual_rent]

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

def investor_calculation_house_data(user, index, property_data, suburb_performance_statistics):
    monthly_decimal_rate=(user.mortgage_interest/100)/12
    if user.variable_loan_type=='Interest Only':
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(user.lvr/100)*monthly_decimal_rate,2)
    else:
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(user.lvr/100)*((monthly_decimal_rate*(1+monthly_decimal_rate)**(12*user.loan_term))/((1+monthly_decimal_rate)**(12*user.loan_term)-1)),2)
        
    property_data[index]['Rental Income']=suburb_performance_statistics.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][3]
    property_data[index]['Operating Expenses']=round(0.50*property_data[index]['Rental Income'],2) #50% rule for calculating operating expenses
    property_data[index]['Cash Flow']=round(property_data[index]['Rental Income']-property_data[index]['Mortgage Repayments']-property_data[index]['Operating Expenses'],2)
    property_data[index]['Cash on Cash Return']=round((property_data[index]['Cash Flow']*12/((1-(user.lvr/100.00))*property_data[index]['Price'])),2)
    property_data[index]['1yr Appreciation']=suburb_performance_statistics.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][0]
    property_data[index]['5yr Appreciation']=suburb_performance_statistics.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][1]
    property_data[index]['10yr Appreciation']=suburb_performance_statistics.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][2]

def investor_calculation_apartment_data(user, index, property_data, suburb_performance_statistics):
    monthly_decimal_rate=(user.mortgage_interest/100)/12
    if user.variable_loan_type=='Interest Only':
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(user.lvr/100)*monthly_decimal_rate,2)
    else:
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(user.lvr/100)*((monthly_decimal_rate*(1+monthly_decimal_rate)**(12*user.loan_term))/((1+monthly_decimal_rate)**(12*user.loan_term)-1)),2)
        
    property_data[index]['Rental Income']=suburb_performance_statistics.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][3]
    property_data[index]['Operating Expenses']=round(0.50*property_data[index]['Rental Income'],2) #50% rule for calculating operating expenses
    property_data[index]['Cash Flow']=round(property_data[index]['Rental Income']-property_data[index]['Mortgage Repayments']-property_data[index]['Operating Expenses'],2)
    property_data[index]['Cash on Cash Return']=round((property_data[index]['Cash Flow']*12/((1-(user.lvr/100.00))*property_data[index]['Price'])),2)
    property_data[index]['1yr Appreciation']=suburb_performance_statistics.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][0]
    property_data[index]['5yr Appreciation']=suburb_performance_statistics.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][1]
    property_data[index]['10yr Appreciation']=suburb_performance_statistics.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][2]

def owner_occupier_calculation_house_data(user, index, property_data,suburb_performance_statistics):
    monthly_decimal_rate=(user.mortgage_interest/100)/12
    if user.variable_loan_type=='Interest Only':
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(user.lvr/100)*monthly_decimal_rate,2)
    else:
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(user.lvr/100)*((monthly_decimal_rate*(1+monthly_decimal_rate)**(12*user.loan_term))/((1+monthly_decimal_rate)**(12*user.loan_term)-1)),2)
    
    property_data[index]['10yr Appreciation']=suburb_performance_statistics.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][2]

def owner_occupier_calculation_apartment_data(user,index,property_data,suburb_performance_statistics):
    monthly_decimal_rate=(user.mortgage_interest/100)/12
    if user.variable_loan_type=='Interest Only':
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(user.lvr/100)*monthly_decimal_rate,2)
    else:
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(user.lvr/100)*((monthly_decimal_rate*(1+monthly_decimal_rate)**(12*user.loan_term))/((1+monthly_decimal_rate)**(12*user.loan_term)-1)),2)
    
    property_data[index]['10yr Appreciation']=suburb_performance_statistics.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][2]



