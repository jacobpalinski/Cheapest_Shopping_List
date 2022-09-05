import requests
import re
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from io import StringIO

# Keys in the form (loan type,lvr,loan term). Average per loan term for variable rates were not found so overall averages where used
# Statistics are retrieved from https://www.savings.com.au/home-loans/home-loan-statistics and periodically updated
# Variable-IO >80 for owner occupier and investor where estimated using best available information
owner_occupier_rate_information={('fixed','=<3'):3.69,('fixed','>3'):4.54,('variable-PI','=<80'):3.07,
('variable-PI','>80'):3.37,('variable-IO','=<80'):3.82,('variable-IO','>80'):4.12}
investor_rate_information={('fixed','=<3'):4.00,('fixed','>3'):4.73,('variable-PI','=<80'):3.42,
('variable-PI','>80'):3.72,('variable-IO','=<80'):3.63,('variable-IO','>80'):3.93}

#Suburb and state data from census to validate suburb exists
reader=csv.DictReader(open(r'australian_suburbs.csv'))
suburb_state_dict={rows['suburb']:rows['state'] for rows in reader if rows['suburb']!='' if rows['state']!=''}

#Used to store all relevant property information extracted
property_data=[]

#Base Class
class User:
    def __init__(self):
        self.locations=[] #Elements are {suburb:state} pairs
        self.property_types=None
        self.bedrooms=None
        self.bathrooms=None
        self.car_spaces=None
        self.date_posted=None # earliest date listing was posted
        self.max_price=None # maximum of price range for home buyer/investor and weekly rental range for renter
        self.min_price=None # minimum of price range for home buyer/investor and weekly rental range for renter
    
class Renter(User):
    pass

class Investor(User):
    def __init__(self):
        super().__init__()
        self.loan_type=None
        self.variable_loan_type=None
        self.lvr=None
        self.loan_term=None
        self.mortgage_interest=None

    #Calculate mortgage interest for fixed rate loans
    def fixed_loan_rate(self,investor_rate_information):
        if self.loan_term<=3:
            self.mortgage_interest=investor_rate_information[('fixed','=<3')]
        elif self.loan_term>3:
            self.mortgage_interest=investor_rate_information[('fixed','>3')]
    
    #Calculate mortgage interest for variable rate loans
    def variable_loan_rate(self,investor_rate_information):
        if self.variable_loan_type=='Principal and Interest':
            if self.lvr<=80:
                self.mortgage_interest=investor_rate_information[('variable-PI','=<80')]
            elif self.lvr>80:
                self.mortgage_interest=investor_rate_information[('variable-PI','>80')]

        elif self.variable_loan_type=='Interest Only':
            if self.lvr<=80:
                self.mortgage_interest=investor_rate_information[('variable-IO','=<80')]
            elif self.lvr>80:
                self.mortgage_interest=investor_rate_information[('variable-IO','>80')]

class Owner_Occupier(Investor,User):
    def __init__(self):
        super().__init__()
    
    #Calculate mortgage interest for fixed rate loans
    def fixed_loan_rate(self,owner_occupier_rate_information):
        if self.loan_term<=3:
            self.mortgage_interest=owner_occupier_rate_information[('fixed','=<3')]
        elif self.loan_term>3:
            self.mortgage_interest=owner_occupier_rate_information[('fixed','>3')]
    
    #Calculate mortgage interest for variable rate loans
    def variable_loan_rate(self,owner_occupier_rate_information):
        if self.variable_loan_type=='Principal and Interest':
            if self.lvr<=80:
                self.mortgage_interest=owner_occupier_rate_information[('variable-PI','=<80')]
            elif self.lvr>80:
                self.mortgage_interest=owner_occupier_rate_information[('variable-PI','>80')]

        elif self.variable_loan_type=='Interest Only':
            if self.lvr<=80:
                self.mortgage_interest=owner_occupier_rate_information[('variable-IO','=<80')]
            elif self.lvr>80:
                self.mortgage_interest=owner_occupier_rate_information[('variable-IO','>80')]

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

#Retrieves all listing data from POST /v1/listings/residential/_search/ for each location in json format
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

#Parses json output in Residental_Listings_Search.responses for common data included in emails for all users
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

#Renter specific data
def listings_data_rent(property_data):
    for property in property_data:
        property['Weekly Rent']=property.pop('Price')
        property['Annual Rent']=property['Weekly Rent']*52

#Investor and Owner Occupier specific data
def listings_data_sale(property_data):
    for property in property_data:
        if property['Price']<100:
            property['Price']=property['Price']*1000000  # for display prices that contained millions symbol with number eg. 1.5M
        elif property['Price']<1000:
            property['Price']=property['Price']*1000 # for display prices that contained thousands symbol with number eg. 539K

#Retrieves performance statistics for houses and apartments from GET /v2/suburbPerformanceStatistics/{state}/{suburb}/{postcode}/ for calculations to be performed for Investors and Owner Occupiers
class Suburb_Performance_Statistics:
    def __init__(self):
        self.api_calls_made={} #Prevent repeated API calls
    
    def request_json(self,index,user,api,property_data,parameter):
        suburb_stats=requests.get('https://api.domain.com.au/v2/suburbPerformanceStatistics/' + property_data[index]['State'] + '/' 
        + property_data[index]['Suburb'].replace(' ','%20')+ '/' + property_data[index]['Postcode'] + '?' + f'propertyCategory={parameter}' 
        + '&' + f'bedrooms={user.bedrooms}'+ '&' + 'periodSize=years' + '&' + 'startingPeriodRelativeToCurrent=1' + '&' 
        + 'totalPeriods=11', headers=api.access_token)
        self.suburb_stats_json=suburb_stats.json()
    
    #Retreive and calculate metrics for houses in a specific location in property_data
    def house_statistics(self,index,user,api,property_data):
        self.request_json(index,user,api,property_data,'house')
        median_annual_rent=self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianRentListingPrice']
        median_sale_20212022=self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianSoldPrice']!=None else (self.suburb_stats_json['series']['seriesInfo'][10]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][10]['values']['lowestSoldPrice'])/2
        median_sale_20202021=self.suburb_stats_json['series']['seriesInfo'][9]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][9]['values']['medianSoldPrice']!=None else (self.suburb_stats_json['series']['seriesInfo'][9]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][9]['values']['lowestSoldPrice'])/2
        median_sale_20172018=self.suburb_stats_json['series']['seriesInfo'][5]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][5]['values']['medianSoldPrice']!=None else (self.suburb_stats_json['series']['seriesInfo'][5]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][5]['values']['lowestSoldPrice'])/2
        median_sale_20112012=self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianSoldPrice']!=None else (self.suburb_stats_json['series']['seriesInfo'][0]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][0]['values']['lowestSoldPrice'])/2
        appreciation_1yr=round(100.00*(median_sale_20212022-median_sale_20202021)/median_sale_20202021,2)
        appreciation_5yr=round(100.00*(median_sale_20212022-median_sale_20172018)/median_sale_20172018,2)
        appreciation_10yr=round(100.00*(median_sale_20212022-median_sale_20112012)/median_sale_20112012,2)
        self.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])]=[appreciation_1yr,
        appreciation_5yr,appreciation_10yr,median_annual_rent]
    
    #Retreive and calculate metrics for apartments in a specific location in property_data
    def apartment_statistics(self,index,user,api,property_data):
        self.request_json(index,user,api,property_data,'unit')
        median_annual_rent=self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianRentListingPrice']
        median_sale_20212022=self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianSoldPrice']!=None else (self.suburb_stats_json['series']['seriesInfo'][10]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][10]['values']['lowestSoldPrice'])/2
        median_sale_20202021=self.suburb_stats_json['series']['seriesInfo'][9]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][9]['values']['medianSoldPrice']!=None else (self.suburb_stats_json['series']['seriesInfo'][9]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][9]['values']['lowestSoldPrice'])/2
        median_sale_20172018=self.suburb_stats_json['series']['seriesInfo'][5]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][5]['values']['medianSoldPrice']!=None else (self.suburb_stats_json['series']['seriesInfo'][5]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][5]['values']['lowestSoldPrice'])/2
        median_sale_20112012=self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianSoldPrice']!=None else (self.suburb_stats_json['series']['seriesInfo'][0]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][0]['values']['lowestSoldPrice'])/2
        appreciation_1yr=round(100.00*(median_sale_20212022-median_sale_20202021)/median_sale_20202021,2)
        appreciation_5yr=round(100.00*(median_sale_20212022-median_sale_20172018)/median_sale_20172018,2)
        appreciation_10yr=round(100.00*(median_sale_20212022-median_sale_20112012)/median_sale_20112012,2)
        self.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])]=[appreciation_1yr,
        appreciation_5yr,appreciation_10yr,median_annual_rent]

# Calculation and creation of key metrics for houses in Investor property_data
def investor_calculation_house_data(investor, index, property_data, suburb_performance_statistics):
    monthly_decimal_rate=(investor.mortgage_interest/100)/12
    if investor.variable_loan_type=='Interest Only':
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(investor.lvr/100)*monthly_decimal_rate,2)
    else:
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(investor.lvr/100)*((monthly_decimal_rate*(1+monthly_decimal_rate)**(12*investor.loan_term))/((1+monthly_decimal_rate)**(12*investor.loan_term)-1)),2)
        
    property_data[index]['Rental Income']=round(365*((suburb_performance_statistics.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][3])/7)/12,2)
    property_data[index]['Operating Expenses']=round(0.50*property_data[index]['Rental Income'],2) #50% rule for calculating operating expenses
    property_data[index]['Cash Flow']=round(property_data[index]['Rental Income']-property_data[index]['Mortgage Repayments']-property_data[index]['Operating Expenses'],2)
    property_data[index]['Cash on Cash Return']=round((property_data[index]['Cash Flow']*12/((1-(investor.lvr/100.00))*property_data[index]['Price'])),2)
    property_data[index]['1yr Appreciation']=suburb_performance_statistics.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][0]
    property_data[index]['5yr Appreciation']=suburb_performance_statistics.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][1]
    property_data[index]['10yr Appreciation']=suburb_performance_statistics.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][2]

# Calculation and creation of key metrics for apartments in Investor property_data
def investor_calculation_apartment_data(investor, index, property_data, suburb_performance_statistics):
    monthly_decimal_rate=(investor.mortgage_interest/100)/12
    if investor.variable_loan_type=='Interest Only':
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(investor.lvr/100)*monthly_decimal_rate,2)
    else:
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(investor.lvr/100)*((monthly_decimal_rate*(1+monthly_decimal_rate)**(12*investor.loan_term))/((1+monthly_decimal_rate)**(12*investor.loan_term)-1)),2)
        
    property_data[index]['Rental Income']=round(365*((suburb_performance_statistics.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][3])/7)/12,2)
    property_data[index]['Operating Expenses']=round(0.50*property_data[index]['Rental Income'],2) #50% rule for calculating operating expenses
    property_data[index]['Cash Flow']=round(property_data[index]['Rental Income']-property_data[index]['Mortgage Repayments']-property_data[index]['Operating Expenses'],2)
    property_data[index]['Cash on Cash Return']=round((property_data[index]['Cash Flow']*12/((1-(investor.lvr/100.00))*property_data[index]['Price'])),2)
    property_data[index]['1yr Appreciation']=suburb_performance_statistics.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][0]
    property_data[index]['5yr Appreciation']=suburb_performance_statistics.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][1]
    property_data[index]['10yr Appreciation']=suburb_performance_statistics.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][2]

# Calculation and creation of mortgage repayments and 10yr appreciation for houses in Owner Occupier property_data
def owner_occupier_calculation_house_data(owner_occupier, index, property_data,suburb_performance_statistics):
    monthly_decimal_rate=(owner_occupier.mortgage_interest/100)/12
    if owner_occupier.variable_loan_type=='Interest Only':
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(owner_occupier.lvr/100)*monthly_decimal_rate,2)
    else:
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(owner_occupier.lvr/100)*((monthly_decimal_rate*(1+monthly_decimal_rate)**(12*owner_occupier.loan_term))/((1+monthly_decimal_rate)**(12*owner_occupier.loan_term)-1)),2)
    
    property_data[index]['10yr Appreciation']=suburb_performance_statistics.api_calls_made[('House',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][2]

# Calculation and creation of mortgage repayments and 10yr appreciation for apartments in Owner Occupier property_data
def owner_occupier_calculation_apartment_data(owner_occupier,index,property_data,suburb_performance_statistics):
    monthly_decimal_rate=(owner_occupier.mortgage_interest/100)/12
    if owner_occupier.variable_loan_type=='Interest Only':
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(owner_occupier.lvr/100)*monthly_decimal_rate,2)
    else:
        property_data[index]['Mortgage Repayments']=round(property_data[index]['Price']*(owner_occupier.lvr/100)*((monthly_decimal_rate*(1+monthly_decimal_rate)**(12*owner_occupier.loan_term))/((1+monthly_decimal_rate)**(12*owner_occupier.loan_term)-1)),2)
    
    property_data[index]['10yr Appreciation']=suburb_performance_statistics.api_calls_made[('Apartment',property_data[index]['Suburb'],property_data[index]['State'],property_data[index]['Postcode'])][2]

class Customer_Email:
    def __init__(self,email_address=None,password=None): #Email + Password from session data in flask application
        self.email_address=email_address 
        self.password=password
        self.port=587
        self.smtp_servers={'Gmail':'smtp.gmail.com','Microsoft':'smtp.office365.com'}
        self.property_data_io=None # store property_data csv in StringIO format before sending email
    
    #Convert property_data to csv in StringIO
    def create_csv_attachment(self,property_data):
        property_data_io=StringIO(newline='')
        dict_writer=csv.DictWriter(property_data_io,property_data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(property_data)
        self.property_data_io=property_data_io

    def send_email_renter(self,renter,smtp_server):
        message=MIMEMultipart()
        message['From']=self.email_address
        message['To']=self.email_address
        suburb_set={suburb for location in renter.locations for suburb in location.keys()}
        suburb_string=','.join(suburb_set)
        message['Subject']=f'Rental Properties in {suburb_string} last updated {renter.date_posted}'
        body= f'{renter.bedrooms} bedroom, {renter.bathrooms} bathroom, {renter.car_spaces} car space {", ".join("Apartments" if property_type=="ApartmentUnitFlat" else property_type + "s" for property_type in renter.property_types).lower()} in {",".join({suburb for location in renter.locations for suburb in location.keys()})}, with weekly rents between ${renter.min_price} and ${renter.max_price}, earliest posting date {renter.date_posted}.'
        message.attach(MIMEText(body,"plain"))
        message.attach(MIMEApplication(self.property_data_io.getvalue(),Name='property_data.csv'))
        with smtplib.SMTP(smtp_server,self.port) as server:
            server.starttls()
            server.login(self.email_address,self.password)
            server.sendmail(self.email_address,self.email_address,message.as_string())
            server.quit()
        
    def send_email_investor_owner_occupier(self,user_type,smtp_server):
        message=MIMEMultipart()
        message['From']=self.email_address
        message['To']=self.email_address
        suburb_set={suburb for location in user_type.locations for suburb in location.keys()}
        suburb_string=','.join(suburb_set)
        message['Subject']=f'Investment Properties in {suburb_string} last updated {user_type.date_posted}'
        body= f'{user_type.bedrooms} bedroom, {user_type.bathrooms} bathroom, {user_type.car_spaces} car space {", ".join("Apartments" if property_type=="ApartmentUnitFlat" else property_type + "s" for property_type in user_type.property_types).lower()} in {", ".join({suburb for location in user_type.locations for suburb in location.keys()})}, priced between ${user_type.min_price} and ${user_type.max_price}, earliest posting date {user_type.date_posted}. Key metrics calculated for {user_type.loan_type.lower()} rate {user_type.variable_loan_type.lower() if user_type.variable_loan_type!="None" else ""} loan with an LVR of {user_type.lvr} for {user_type.loan_term} years with {user_type.mortgage_interest}% interest p.a.'
        message.attach(MIMEText(body,"plain"))
        message.attach(MIMEApplication(self.property_data_io.getvalue(),Name='property_data.csv'))
        with smtplib.SMTP(smtp_server,self.port) as server:
            server.starttls()
            server.login(self.email_address,self.password)
            server.sendmail(self.email_address,self.email_address,message.as_string())
            server.quit()