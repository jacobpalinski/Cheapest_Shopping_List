import os
import requests
import re
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from io import StringIO
from dotenv import load_dotenv

# Load environment variables for api access
load_dotenv()

# Keys in the form (loan type,lvr,loan term). Average per loan term for variable rates were not found so overall averages where used
# Statistics are retrieved from https://www.savings.com.au/home-loans/home-loan-statistics using RBA data and periodically updated
# Variable-IO >80 for owner occupier and investor where estimated using best available information
owner_occupier_rate_information = {('fixed','=<3'): 5.53, ('fixed','>3'): 6.05, ('variable-PI','=<80'): 5.39,
('variable-PI','>80'): 5.69, ('variable-IO','=<80'): 6.04, ('variable-IO','>80'): 6.34}
investor_rate_information = {('fixed','=<3'): 5.75, ('fixed','>3'): 6.60, ('variable-PI','=<80'): 5.70,
('variable-PI','>80'): 6.04, ('variable-IO','=<80'): 5.90, ('variable-IO','>80'): 6.20}

# Suburb and state data from census to validate suburb exists
reader = csv.DictReader(open(r'C:\Users\kpali\Documents\Projects\Property_Notifier\australian_suburbs.csv'))
suburb_state_dict = {(rows['suburb'],rows['state'],rows['postcode']): 1 for rows in reader if rows['suburb'] != '' if rows['state'] != '' if rows['postcode'] != ''}

# Base Class
class User:
    def __init__(self):
        self.locations = [] # Fix comment
        self.property_types = None
        self.bedrooms = None
        self.bathrooms = None
        self.car_spaces = None
        self.date_posted = None # Earliest date listing was posted
        self.max_price = None # Maximum of price range for owner occupier/investor and weekly rental range for renter
        self.min_price = None # Minimum of price range for owner occupier/investor and weekly rental range for renter
    
class Renter(User):
    pass

class Investor(User):
    def __init__(self):
        super().__init__()
        self.loan_type = None
        self.variable_loan_type = None
        self.lvr = None
        self.loan_term = None
        self.mortgage_interest = None

    # Calculate mortgage interest for fixed rate loans
    def fixed_loan_rate(self, investor_rate_information):
        if self.loan_term <= 3:
            self.mortgage_interest = investor_rate_information[('fixed','=<3')]
        elif self.loan_term > 3:
            self.mortgage_interest = investor_rate_information[('fixed','>3')]
    
    # Calculate mortgage interest for variable rate loans
    def variable_loan_rate(self, investor_rate_information):
        if self.variable_loan_type == 'Principal and Interest':
            if self.lvr <= 80:
                self.mortgage_interest = investor_rate_information[('variable-PI','=<80')]
            elif self.lvr > 80:
                self.mortgage_interest = investor_rate_information[('variable-PI','>80')]

        elif self.variable_loan_type == 'Interest Only':
            if self.lvr <= 80:
                self.mortgage_interest = investor_rate_information[('variable-IO','=<80')]
            elif self.lvr > 80:
                self.mortgage_interest = investor_rate_information[('variable-IO','>80')]

class OwnerOccupier(Investor,User):
    def __init__(self):
        super().__init__()
    
    # Calculate mortgage interest for fixed rate loans
    def fixed_loan_rate(self, owner_occupier_rate_information):
        if self.loan_term <= 3:
            self.mortgage_interest = owner_occupier_rate_information[('fixed','=<3')]
        elif self.loan_term > 3:
            self.mortgage_interest = owner_occupier_rate_information[('fixed','>3')]
    
    # Calculate mortgage interest for variable rate loans
    def variable_loan_rate(self, owner_occupier_rate_information):
        if self.variable_loan_type == 'Principal and Interest':
            if self.lvr <= 80:
                self.mortgage_interest = owner_occupier_rate_information[('variable-PI','=<80')]
            elif self.lvr > 80:
                self.mortgage_interest = owner_occupier_rate_information[('variable-PI','>80')]

        elif self.variable_loan_type == 'Interest Only':
            if self.lvr <= 80:
                self.mortgage_interest = owner_occupier_rate_information[('variable-IO','=<80')]
            elif self.lvr > 80:
                self.mortgage_interest = owner_occupier_rate_information[('variable-IO','>80')]

class APIClient:
    CLIENT_ID = str(os.environ.get('CLIENT_ID'))
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))
    SCOPE = ['api_listings_read api_suburbperformance_read']

    def generate_token(self):
        response = requests.post(f'https://auth.domain.com.au/v1/connect/token', {'client_id': APIClient.CLIENT_ID,
        'client_secret': APIClient.SECRET_KEY, 
        'grant_type': 'client_credentials',
        'scope': APIClient.SCOPE,
        'Content-Type': 'application/json'})
        self.access_token = {'Authorization': 'Bearer ' + response.json()['access_token']}

# Retrieves all listing data from POST /v1/listings/residential/_search/ for each location in json format
class ResidentialListingsSearch:
    def __init__(self,user, api_client):
        self.user = user
        self.api_client = api_client
        self.responses = [] # Stores json responses for each location
    
    def listings_request(self):
        for location in self.user.locations:
            suburb, state, postcode = location
            listings = requests.post('https://api.domain.com.au/v1/listings/residential/_search', json = {
                'listingType': 'Rent' if isinstance(self.user, Renter) else 'Sale',
                'propertyTypes': self.user.property_types,
                'minBedrooms': self.user.bedrooms,
                'minBathrooms': self.user.bathrooms,
                'minCarspaces': self.user.car_spaces,
                'minPrice': self.user.min_price,
                'maxPrice': self.user.max_price,
                'locations': [
                    {
                        'state': state,
                        'region': '',
                        'area': '',
                        'suburb': suburb,
                        'postcode': postcode,
                        'includeSurroundingSuburbs': False        
                    }
                ],
                'excludePriceWithheld': False,
                'excludeDepositTaken': True,
                'pageSize': 50,
                'listedSince': f'{self.user.date_posted}'}, headers = self.api_client.access_token)
            
            self.responses.append(listings.json())

# Stores and retrieves property listing data from Residential_Listings_Search
class PropertyData:
    def __init__(self, residential_listings_search):
        self.residential_listings_search = residential_listings_search
        self.data = []
    
    # Parses json outputs in Residential_Listings for common data included in csv for renters, owner occupiers and investors
    def common_listings_data(self):
        for listings_json in self.residential_listings_search.responses:
            for properties in listings_json:
                if properties['type'] == 'PropertyListing':
                    date_listing = re.search(r'[\d-]+', properties['listing']['dateListed']).group(0)
                    type = properties['listing']['propertyDetails']['propertyType']
                    suburb = properties['listing']['propertyDetails']['suburb'].lower().title()
                    state = properties['listing']['propertyDetails']['state']
                    postcode = properties['listing']['propertyDetails']['postcode']
                    address = properties['listing']['propertyDetails']['displayableAddress']
                    area = properties['listing']['propertyDetails']['landArea'] if properties['listing']['propertyDetails'].get('landArea') else 'N/A'
                    display_price_search = re.search(r'(\d+(\.\d*)?)+', properties['listing']['priceDetails']['displayPrice'].replace(',',''))
                    url = 'https://www.domain.com.au/' + properties['listing']['listingSlug']
                    if display_price_search == None:
                        display_price = self.residential_listings_search.user.min_price
                    else:
                        display_price = float(display_price_search.group(0))
                    self.data.append({'Listing Date': date_listing, 'Property Type': type, 'Suburb': suburb, 'State': state,
                    'Postcode': postcode, 'Address': address, 'Land Area': area, 'Price': display_price, 'Url': url})

    # Weekly and annual rent data (only for renters)
    def listings_data_rent(self):
        for property in self.data:
            property['Weekly Rent'] = property.pop('Price')
            property['Annual Rent'] = property['Weekly Rent'] * 52

    # Convert property listings with prices that contain symbols into integers (only for investors and owner occupiers)
    def listings_data_sale(self):
        for property in self.data:
            if property['Price'] < 100:
                property['Price'] = property['Price'] * 1000000  # for display prices that contained millions symbol with number eg. 1.5M
            elif property['Price'] < 1000:
                property['Price'] = property['Price'] * 1000  # for display prices that contained thousands symbol with number eg. 539K

# Retrieves performance statistics for houses and apartments from GET /v2/suburbPerformanceStatistics/{state}/{suburb}/{postcode}/ and calculates statistics for Investors and Owner Occupiers
class SuburbPerformanceStatistics:
    def __init__(self,user, api_client, property_data):
        self.user = user
        self.api_calls_made = {} # Prevent repeated API calls
        self.api_client = api_client
        self.data = property_data.data
    
    def request_json(self, index, property_category):
        suburb_stats = requests.get('https://api.domain.com.au/v2/suburbPerformanceStatistics/' + self.data[index]['State'] + '/' 
        + self.data[index]['Suburb'].replace(' ','%20') + '/' + self.data[index]['Postcode'] + '?' + f'propertyCategory={property_category}' 
        + '&' + f'bedrooms={self.user.bedrooms}' + '&' + 'periodSize=years' + '&' + 'startingPeriodRelativeToCurrent=1' + '&' 
        + 'totalPeriods=11', headers = self.api_client.access_token)
        self.suburb_stats_json = suburb_stats.json()
    
    # Retreive and calculate metrics for houses in a specific location in property_data
    def house_statistics(self, index):
        self.request_json(index, 'house')
        median_annual_rent = self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianRentListingPrice']
        median_sale_20222023 = self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianSoldPrice'] != None else (self.suburb_stats_json['series']['seriesInfo'][10]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][10]['values']['lowestSoldPrice']) / 2
        median_sale_20212022 = self.suburb_stats_json['series']['seriesInfo'][9]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][9]['values']['medianSoldPrice'] != None else (self.suburb_stats_json['series']['seriesInfo'][9]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][9]['values']['lowestSoldPrice']) / 2
        median_sale_20182019 = self.suburb_stats_json['series']['seriesInfo'][5]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][5]['values']['medianSoldPrice'] != None else (self.suburb_stats_json['series']['seriesInfo'][5]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][5]['values']['lowestSoldPrice']) / 2
        median_sale_20122013 = self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianSoldPrice'] != None else (self.suburb_stats_json['series']['seriesInfo'][0]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][0]['values']['lowestSoldPrice']) / 2
        appreciation_1yr = round(100.00 * (median_sale_20222023 - median_sale_20212022) / median_sale_20212022, 2)
        appreciation_5yr = round(100.00 * (median_sale_20222023 - median_sale_20182019) / median_sale_20182019, 2)
        appreciation_10yr = round(100.00 * (median_sale_20222023 - median_sale_20122013) / median_sale_20122013, 2)
        self.api_calls_made[('House',self.data[index]['Suburb'],self.data[index]['State'],self.data[index]['Postcode'])] = [appreciation_1yr,
        appreciation_5yr, appreciation_10yr, median_annual_rent]
    
    # Retreive and calculate metrics for apartments in a specific location in property_data
    def apartment_statistics(self, index):
        self.request_json(index, 'unit') # API classes apartments under the parameter 'unit'
        median_annual_rent = self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianRentListingPrice']
        median_sale_20212022 = self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][10]['values']['medianSoldPrice'] != None else (self.suburb_stats_json['series']['seriesInfo'][10]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][10]['values']['lowestSoldPrice']) / 2
        median_sale_20202021 = self.suburb_stats_json['series']['seriesInfo'][9]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][9]['values']['medianSoldPrice'] != None else (self.suburb_stats_json['series']['seriesInfo'][9]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][9]['values']['lowestSoldPrice']) / 2
        median_sale_20172018 = self.suburb_stats_json['series']['seriesInfo'][5]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][5]['values']['medianSoldPrice'] != None else (self.suburb_stats_json['series']['seriesInfo'][5]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][5]['values']['lowestSoldPrice']) / 2
        median_sale_20112012 = self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianSoldPrice'] if self.suburb_stats_json['series']['seriesInfo'][0]['values']['medianSoldPrice'] != None else (self.suburb_stats_json['series']['seriesInfo'][0]['values']['highestSoldPrice'] - self.suburb_stats_json['series']['seriesInfo'][0]['values']['lowestSoldPrice']) / 2
        appreciation_1yr = round(100.00 * (median_sale_20212022 - median_sale_20202021) / median_sale_20202021, 2)
        appreciation_5yr = round(100.00 * (median_sale_20212022 - median_sale_20172018) / median_sale_20172018, 2)
        appreciation_10yr = round(100.00 * (median_sale_20212022 - median_sale_20112012) / median_sale_20112012, 2)
        self.api_calls_made[('Apartment',self.data[index]['Suburb'],self.data[index]['State'],self.data[index]['Postcode'])] = [appreciation_1yr,
        appreciation_5yr, appreciation_10yr, median_annual_rent]
    
    def calculate_investor_metrics(self, index, property_category):
        monthly_decimal_rate = (self.user.mortgage_interest / 100) / 12
        if self.user.variable_loan_type == 'Interest Only':
            self.data[index]['Mortgage Repayments'] = round(self.data[index]['Price'] * (self.user.lvr / 100) * monthly_decimal_rate, 2)
        else:
            self.data[index]['Mortgage Repayments'] = round(self.data[index]['Price'] * (self.user.lvr / 100) * ((monthly_decimal_rate * (1 + monthly_decimal_rate)**(12 * self.user.loan_term)) / ((1 + monthly_decimal_rate)**(12 * self.user.loan_term) - 1)), 2)
            
        self.data[index]['Rental Income'] = round(365 * ((self.api_calls_made[(property_category,self.data[index]['Suburb'],self.data[index]['State'],self.data[index]['Postcode'])][3]) / 7) / 12, 2)
        self.data[index]['Operating Expenses'] = round(0.50 * self.data[index]['Rental Income'],2) # 50% rule for calculating operating expenses
        self.data[index]['Cash Flow'] = round(self.data[index]['Rental Income'] - self.data[index]['Mortgage Repayments'] - self.data[index]['Operating Expenses'], 2)
        self.data[index]['Cash on Cash Return'] = round((self.data[index]['Cash Flow'] * 12 / ((1 - (self.user.lvr / 100.00)) * self.data[index]['Price'])), 2)
        self.data[index]['1yr Appreciation'] = self.api_calls_made[(property_category,self.data[index]['Suburb'],self.data[index]['State'],self.data[index]['Postcode'])][0]
        self.data[index]['5yr Appreciation'] = self.api_calls_made[(property_category,self.data[index]['Suburb'],self.data[index]['State'],self.data[index]['Postcode'])][1]
        self.data[index]['10yr Appreciation'] = self.api_calls_made[(property_category,self.data[index]['Suburb'],self.data[index]['State'],self.data[index]['Postcode'])][2]

    def calculate_owner_occupier_metrics(self, index, property_category):
        monthly_decimal_rate = (self.user.mortgage_interest / 100) / 12
        if self.user.variable_loan_type == 'Interest Only':
            self.data[index]['Mortgage Repayments'] = round(self.data[index]['Price'] * (self.user.lvr / 100) * monthly_decimal_rate, 2)
        else:
            self.data[index]['Mortgage Repayments'] = round(self.data[index]['Price'] * (self.user.lvr / 100) * ((monthly_decimal_rate * (1 + monthly_decimal_rate)**(12 * self.user.loan_term)) / ((1 + monthly_decimal_rate)**(12 * self.user.loan_term) - 1)), 2)
        
        self.data[index]['10yr Appreciation'] = self.api_calls_made[(property_category,self.data[index]['Suburb'],self.data[index]['State'],self.data[index]['Postcode'])][2]

class CustomerEmail:
    def __init__(self, property_data = None, suburb_performance_statistics = None, email_address = None, password = None): # Email + Password from session data in flask application
        if suburb_performance_statistics != None:
            self.user = suburb_performance_statistics.user
            self.data = suburb_performance_statistics.data
        elif property_data != None:
            self.user = property_data.residential_listings_search.user
            self.data = property_data.data
        self.email_address = email_address 
        self.password = password
        self.port = 587
        self.smtp_servers = {'Gmail': 'smtp.gmail.com', 'Microsoft': 'smtp.office365.com'}
        self.data_io = None # store csv in StringIO format before sending email
    
    # Convert property_data to csv in StringIO
    def create_csv_attachment(self):
        data_io = StringIO(newline = '')
        dict_writer = csv.DictWriter(data_io, self.data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(self.data)
        self.data_io = data_io

    def send_email_renter(self, smtp_server):
        message = MIMEMultipart()
        message['From'] = self.email_address
        message['To'] = self.email_address
        suburb_set = {location[0] for location in self.user.locations} # Extracts suburb from each location tuple in self.user.locations
        suburb_string = ','.join(suburb_set)
        message['Subject'] = f'Rental Properties in {suburb_string} last updated {self.user.date_posted}'
        body = f'{self.user.bedrooms} bedroom, {self.user.bathrooms} bathroom, {self.user.car_spaces} car space {", ".join("Apartments" if property_type == "ApartmentUnitFlat" else property_type + "s" for property_type in self.user.property_types).lower()} in {suburb_string}, with weekly rents between ${self.user.min_price} and ${self.user.max_price}, earliest posting date {self.user.date_posted}.'
        message.attach(MIMEText(body, "plain"))
        message.attach(MIMEApplication(self.data_io.getvalue(), Name = 'property_data.csv'))
        with smtplib.SMTP(smtp_server, self.port) as server:
            server.starttls()
            server.login(self.email_address, self.password)
            server.sendmail(self.email_address, self.email_address, message.as_string())
            server.quit()
        
    def send_email_investor_owner_occupier(self, smtp_server):
        message = MIMEMultipart()
        message['From'] = self.email_address
        message['To'] = self.email_address
        suburb_set = {location[0] for location in self.user.locations} # Extracts suburb from each location tuple in self.user.locations
        suburb_string = ','.join(suburb_set)
        print(self.user.variable_loan_type)
        print(type(self.user.variable_loan_type))
        message['Subject'] = f'{"Properties for Sale" if isinstance(self.user, OwnerOccupier) else "Investment Properties"} in {suburb_string} last updated {self.user.date_posted}'
        body= f'{self.user.bedrooms} bedroom, {self.user.bathrooms} bathroom, {self.user.car_spaces} car space {", ".join("Apartments" if property_type == "ApartmentUnitFlat" else property_type + "s" for property_type in self.user.property_types).lower()} in {suburb_string}, priced between ${self.user.min_price} and ${self.user.max_price}, earliest posting date {self.user.date_posted}. Key metrics calculated for {self.user.loan_type} Rate {self.user.variable_loan_type if self.user.variable_loan_type != "None" else ""} Loan with an LVR of {self.user.lvr} for {self.user.loan_term} years with a {self.user.mortgage_interest}% interest rate p.a.'.replace("Rate  Loan", "Rate Loan")
        message.attach(MIMEText(body, "plain"))
        message.attach(MIMEApplication(self.data_io.getvalue(), Name = 'property_data.csv'))
        with smtplib.SMTP(smtp_server,self.port) as server:
            server.starttls()
            server.login(self.email_address,self.password)
            server.sendmail(self.email_address,self.email_address,message.as_string())
            server.quit()