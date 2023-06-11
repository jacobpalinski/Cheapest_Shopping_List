import pytest
import requests
import requests_mock
import json
import pytest_mock
from property_notifier import *

class TestMortgageInterestFunctionsInvestor:
    def test_investor_fixed_rate_loan_term_2yr(self):
        investor = Investor()
        investor.loan_type = 'Fixed'
        investor.variable_loan_type = None
        investor.lvr = 80
        investor.loan_term = 2
        investor.fixed_loan_rate(investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == investor_rate_information[('fixed','=<3')]

    def test_investor_fixed_rate_loan_term_5yr(self):
        investor = Investor()
        investor.loan_type = 'Fixed'
        investor.variable_loan_type = None
        investor.lvr = 80
        investor.loan_term = 5
        investor.fixed_loan_rate(investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == investor_rate_information[('fixed','>3')]
    
    def test_investor_variable_rate_principal_and_interest_lvr_80_loan_term_10yr(self):
        investor = Investor()
        investor.loan_type = 'Variable'
        investor.variable_loan_type = 'Principal and Interest'
        investor.lvr = 80
        investor.loan_term = 10
        investor.variable_loan_rate(investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == investor_rate_information[('variable-PI','=<80')]
    
    def test_investor_variable_rate_principal_and_interest_lvr_90_loan_term_10yr(self):
        investor = Investor()
        investor.loan_type = 'Variable'
        investor.variable_loan_type = 'Principal and Interest'
        investor.lvr = 90
        investor.loan_term = 10
        investor.variable_loan_rate(investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == investor_rate_information[('variable-PI','>80')]
    
    def test_investor_variable_rate_interest_only_lvr_80_loan_term_10yr(self):
        investor = Investor()
        investor.loan_type = 'Variable'
        investor.variable_loan_type = 'Interest Only'
        investor.lvr = 80
        investor.loan_term = 10
        investor.variable_loan_rate(investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == investor_rate_information[('variable-IO','=<80')]
    
    def test_investor_variable_rate_interest_only_lvr_90_loan_term_10yr(self):
        investor = Investor()
        investor.loan_type = 'Variable'
        investor.variable_loan_type = 'Interest Only'
        investor.lvr = 90
        investor.loan_term = 10
        investor.variable_loan_rate(investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == investor_rate_information[('variable-IO','>80')]

class TestMortgageInterestFunctionsOwnerOccupier:
    def test_owner_occupier_fixed_rate_loan_term_2yr(self):
        owner_occupier = OwnerOccupier()
        owner_occupier.loan_type = 'Fixed'
        owner_occupier.variable_loan_type = None
        owner_occupier.lvr = 80
        owner_occupier.loan_term = 2
        owner_occupier.fixed_loan_rate(owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == owner_occupier_rate_information[('fixed','=<3')]

    def test_owner_occupier_fixed_rate_loan_term_5yr(self):
        owner_occupier = OwnerOccupier()
        owner_occupier.loan_type = 'Fixed'
        owner_occupier.variable_loan_type = None
        owner_occupier.lvr = 80
        owner_occupier.loan_term = 5
        owner_occupier.fixed_loan_rate(owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == owner_occupier_rate_information[('fixed','>3')]
    
    def test_owner_occupier_variable_rate_principal_and_interest_lvr_80_loan_term_10yr(self):
        owner_occupier = OwnerOccupier()
        owner_occupier.loan_type = 'Variable'
        owner_occupier.variable_loan_type = 'Principal and Interest'
        owner_occupier.lvr = 80
        owner_occupier.loan_term = 10
        owner_occupier.variable_loan_rate(owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == owner_occupier_rate_information[('variable-PI','=<80')]
    
    def test_owner_occupier_variable_rate_principal_and_interest_lvr_90_loan_term_10yr(self):
        owner_occupier = OwnerOccupier()
        owner_occupier.loan_type = 'Variable'
        owner_occupier.variable_loan_type = 'Principal and Interest'
        owner_occupier.lvr = 90
        owner_occupier.loan_term = 10
        owner_occupier.variable_loan_rate(owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == owner_occupier_rate_information[('variable-PI','>80')]
    
    def test_owner_occupier_variable_rate_interest_only_lvr_80_loan_term_10yr(self):
        owner_occupier = OwnerOccupier()
        owner_occupier.loan_type = 'Variable'
        owner_occupier.variable_loan_type = 'Interest Only'
        owner_occupier.lvr = 80
        owner_occupier.loan_term = 10
        owner_occupier.variable_loan_rate(owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == owner_occupier_rate_information[('variable-IO','=<80')]
    
    def test_owner_occupier_variable_rate_interest_only_lvr_90_loan_term_10yr(self):
        owner_occupier = OwnerOccupier()
        owner_occupier.loan_type = 'Variable'
        owner_occupier.variable_loan_type = 'Interest Only'
        owner_occupier.lvr = 90
        owner_occupier.loan_term = 10
        owner_occupier.variable_loan_rate(owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == owner_occupier_rate_information[('variable-IO','>80')]

class TestAccessToken:
    def test_connection(self):
        with requests_mock.mock() as m:
            m.post('https://auth.domain.com.au/v1/connect/token', json = {'access_token': 'token', 'expires_in': 43200, 'token_type': 'Bearer'})
            response=requests.post('https://auth.domain.com.au/v1/connect/token', data = {'client_id': APIClient.CLIENT_ID,
            'client_secret': APIClient.SECRET_KEY, 'grant_type': 'client_credentials', 'scope': APIClient.SCOPE, 'Content-Type': 'text/json'})
            assert response.json()['access_token'] == 'token'

@pytest.fixture
def renter():
    renter = Renter()
    renter.locations = [('Hurstville', 'NSW', 2220), ('Penshurst','NSW', 2222)]
    renter.property_types = ['House', 'Apartment']
    renter.bedrooms = 3
    renter.bathrooms = 2
    renter.car_spaces = 2
    renter.date_posted = '2022-06-17'
    renter.min_price = 500
    renter.max_price = 800
    return renter

@pytest.fixture
def investor():
    investor = Investor()
    investor.locations = [('Hurstville', 'NSW', 2220), ('Penshurst', 'NSW', 2222)]
    investor.property_types = ['House', 'Apartment']
    investor.bedrooms = 3
    investor.bathrooms = 2
    investor.car_spaces = 2
    investor.date_posted = '2022-06-17'
    investor.min_price = 500
    investor.max_price = 800
    investor.loan_type = 'Variable'
    investor.variable_loan_type = 'Principal and Interest'
    investor.lvr = 80
    investor.loan_term = 10
    investor.mortgage_interest = 3.42
    return investor

@pytest.fixture
def owner_occupier():
    owner_occupier = OwnerOccupier()
    owner_occupier.locations = [('Hurstville', 'NSW', 2220),('Penshurst', 'NSW', 2222)]
    owner_occupier.property_types = ['House', 'Apartment']
    owner_occupier.bedrooms = 3
    owner_occupier.bathrooms = 2
    owner_occupier.car_spaces = 2
    owner_occupier.date_posted = '2022-06-17'
    owner_occupier.min_price = 500
    owner_occupier.max_price = 800
    owner_occupier.loan_type = 'Variable'
    owner_occupier.variable_loan_type = 'Principal and Interest'
    owner_occupier.lvr = 80
    owner_occupier.loan_term = 10
    owner_occupier.mortgage_interest = 3.07
    return owner_occupier

@pytest.fixture
def api_client():
    api_client = APIClient()
    api_client.access_token = 'token'
    return api_client

@pytest.fixture
def residential_listings_search_renter(renter, api_client):
    residential_listings_search = ResidentialListingsSearch(renter, api_client)
    return residential_listings_search

@pytest.fixture
def residential_listings_search_investor(investor, api_client):
    residential_listings_search = ResidentialListingsSearch(investor, api_client)
    return residential_listings_search

@pytest.fixture
def residential_listings_search_owner_occupier(owner_occupier, api_client):
    residential_listings_search = ResidentialListingsSearch(owner_occupier, api_client)
    return residential_listings_search

class TestListingsRequest:
    @pytest.mark.parametrize('residential_listings_search, expected_json_response',
    [(pytest.lazy_fixture('residential_listings_search_renter'), [{'type': "PropertyListing", 'listing': {'listingType': 'Rent'}}]),
    (pytest.lazy_fixture('residential_listings_search_investor'), [{'type': "PropertyListing", 'listing': {'listingType': 'Sale'}}]),
    (pytest.lazy_fixture('residential_listings_search_owner_occupier'), [{'type': "PropertyListing", 'listing': {'listingType': 'Sale'}}])])
    def test_listings_request_renter(self,residential_listings_search, expected_json_response):
        for location in residential_listings_search.user.locations:
            for suburb, state, postcode in [location[:]]:
                with requests_mock.mock() as m:
                    m.post('https://api.domain.com.au/v1/listings/residential/_search', json = [{'type': "PropertyListing",
                    "listing": {"listingType": "Rent"}}])
                    response = requests.post('https://api.domain.com.au/v1/listings/residential/_search',json = {
                        'listingType': 'Rent' if isinstance(residential_listings_search.user, Renter) else 'Sale',
                        'propertyTypes': residential_listings_search.user.property_types,
                        'minBedrooms': residential_listings_search.user.bedrooms,
                        'minBathrooms': residential_listings_search.user.bathrooms,
                        'minCarspaces': residential_listings_search.user.car_spaces,
                        'minPrice': residential_listings_search.user.min_price,
                        'maxPrice': residential_listings_search.user.max_price,
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
                        'listedSince': f'{residential_listings_search.user.date_posted}'}, headers = {'Authorization': 'Bearer ' + residential_listings_search.api_client.access_token})
                    if isinstance(residential_listings_search.user, Renter):
                        assert response.json() == expected_json_response
                    else:
                        assert response.json() != expected_json_response

@pytest.fixture(params = ["House", "Apartment"])
def residential_listings_response(request):
    response = [
  {
    "type": "PropertyListing",
    "listing": {
      "id": 15970998,
      "advertiser": {
        "type": "Agency",
        "id": 25306,
        "name": "Morton Green Square",
        "logoUrl": "https://images.domain.com.au/img/Agencys/25306/logo_25306.GIF?date=2015-03-25-17-35-45",
        "preferredColourHex": "#01325A",
        "bannerUrl": "https://images.domain.com.au/img/Agencys/25306/banner_25306.GIF",
        "contacts": [
          {
            "name": "Kristian Karaspyros",
            "photoUrl": "https://images.domain.com.au/img/25306/contact_1828499.jpeg?mod=220725-185822"
          },
          {
            "name": "Ayush Jain",
            "photoUrl": "https://images.domain.com.au/img/25306/contact_1547925.jpeg?mod=220725-185822"
          }
        ]
      },
      "priceDetails": {
        "displayPrice": "$715 per week"
      },
      "media": [
        {
          "category": "Image",
          "url": "https://bucket-api.domain.com.au/v1/bucket/image/15970998_1_1_220705_080432-w2667-h1778"
        },
        {
          "category": "Image",
          "url": "https://bucket-api.domain.com.au/v1/bucket/image/15970998_2_1_220705_080432-w2667-h1778"
        },
        {
          "category": "Image",
          "url": "https://bucket-api.domain.com.au/v1/bucket/image/15970998_3_1_220705_080432-w3840-h2560"
        },
        {
          "category": "Image",
          "url": "https://bucket-api.domain.com.au/v1/bucket/image/15970998_4_1_220705_080432-w2667-h1778"
        },
        {
          "category": "Image",
          "url": "https://bucket-api.domain.com.au/v1/bucket/image/15970998_5_1_220705_080432-w3200-h2133"
        }
      ],
      "propertyDetails": {
        "state": "NSW",
        "features": [
          "Floorboards"
        ],
        "propertyType": request.param,
        "allPropertyTypes": [
          "House"
        ],
        "bathrooms": 2,
        "bedrooms": 3,
        "carspaces": 2,
        "unitNumber": "",
        "streetNumber": "94",
        "street": "Queens Road",
        "area": "St George",
        "region": "Sydney Region",
        "suburb": "HURSTVILLE",
        "postcode": "2220",
        "displayableAddress": "94 Queens Road, Hurstville",
        "latitude": -33.96301,
        "longitude": 151.103256,
        "isRural": False,
        "isNew": False,
        "tags": []
      },
      "headline": "Three Bedroom Home Close to Hurstville CBD",
      "summaryDescription": "<b></b><br />This beautifully presented family home only minutes walking distance to Hurstville Westfields and public transport. The property offers a renovated kitchen ample storage.Two modern bathrooms. Includes 3 very spacious bedrooms with an addit...",
      "hasFloorplan": True,
      "hasVideo": False,
      "labels": [],
      "dateAvailable": "2022-07-28",
      "dateListed": "2022-07-05T18:04:33",
      "inspectionSchedule": {
        "byAppointment": False,
        "recurring": False,
        "times": [
          {
            "openingTime": "2022-07-27T09:30:00",
            "closingTime": "2022-07-27T09:45:00"
          }
        ]
      },
      "listingSlug": "94-queens-road-hurstville-nsw-2220-15970998"
    }
  }]
    return response

@pytest.fixture
def property_data(residential_listings_search_investor, residential_listings_response):
    residential_listings_search_investor.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search_investor)
    return property_data

class TestPropertyData:
    def test_common_listings_data(self, property_data):
        property_data.common_listings_data()
        if property_data.data[0]['Property Type'] == 'House':
            assert property_data.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'House', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998'}
        else:
            assert property_data.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'Apartment', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998'}
    
    def test_listings_data_rent(self, property_data):
        property_data.common_listings_data()
        property_data.listings_data_rent()
        if property_data.data[0]['Property Type'] == 'House':
            assert property_data.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'House', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A',
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Weekly Rent': 715.00, 'Annual Rent': 37180.00}
        else:
            assert property_data.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'Apartment', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A',
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Weekly Rent': 715.00, 'Annual Rent': 37180.00}

    def test_listings_data_sale(self, property_data):
        property_data.common_listings_data()
        property_data.listings_data_sale()
        if property_data.data[0]['Property Type'] == 'House':
            assert property_data.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'House', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715000.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998'}
        else:
            assert property_data.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'Apartment', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715000.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998'}

@pytest.fixture
def suburb_performance_statistics_house(residential_listings_search_investor, residential_listings_response, investor, api_client):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'House':
        pytest.skip('Suburb performance statistics for house only')
    residential_listings_search_investor.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search_investor)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(investor, api_client, property_data)
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_apartment(residential_listings_search_investor, residential_listings_response, investor, api_client):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'Apartment':
        pytest.skip('Suburb performance statistics for apartment only')
    residential_listings_search_investor.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search_investor)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(investor,api_client,property_data)
    return suburb_performance_statistics

@pytest.fixture
def housing_statistics_json():
    house_stats_file = open(r"C:\Users\kpali\Downloads\house_stats_json_testsample.json")
    return json.loads(house_stats_file.read())

@pytest.fixture
def apartment_statistics_json():
    apartment_stats_file = open(r"C:\Users\kpali\Downloads\unit_apartment_stats_json_testsample.json")
    return json.loads(apartment_stats_file.read())

class TestSuburbPerformanceStatistics:
    @pytest.mark.parametrize("suburb_performance_statistics, property_category",
    [(pytest.lazy_fixture('suburb_performance_statistics_house'), 'House'),
    (pytest.lazy_fixture('suburb_performance_statistics_apartment'), 'Apartment')])
    def test_house_request_json(self,suburb_performance_statistics, property_category):
        with requests_mock.mock() as m:
            m.get('https://api.domain.com.au/v2/suburbPerformanceStatistics/NSW/Hurstville/2220?propertyCategory=House&bedrooms=3&periodSize=Years&startingPeriodRelativeToCurrent=1&totalPeriods=11',
            json = {'header': {'suburb': suburb_performance_statistics.data[0]['Suburb'],
            'state': suburb_performance_statistics.data[0]['State'], 'property_category': property_category}})
            response = requests.get('https://api.domain.com.au/v2/suburbPerformanceStatistics/' + suburb_performance_statistics.data[0]['State'] + '/' 
            + suburb_performance_statistics.data[0]['Suburb'].replace(' ','%20')+ '/' + suburb_performance_statistics.data[0]['Postcode'] + '?' 
            + f'propertyCategory=House' 
            + '&' + f'bedrooms={suburb_performance_statistics.user.bedrooms}'+ '&' + 'periodSize=years' + '&' + 'startingPeriodRelativeToCurrent=1' + '&' 
            + 'totalPeriods=11', headers = {'Authorization': 'Bearer ' + suburb_performance_statistics.api_client.access_token})
            if suburb_performance_statistics.data[0]['Property Type'] == 'House':
                assert response.json() == {'header': {'suburb': suburb_performance_statistics.data[0]['Suburb'],
                'state': suburb_performance_statistics.data[0]['State'], 'property_category': 'House'}}
            else:
                assert response.json() == {'header': {'suburb': suburb_performance_statistics.data[0]['Suburb'],
                'state': suburb_performance_statistics.data[0]['State'], 'property_category': 'Apartment'}}

    def test_house_statistics_json(self, housing_statistics_json, suburb_performance_statistics_house, index = 0):
        median_annual_rent = housing_statistics_json['series']['seriesInfo'][10]['values']['medianRentListingPrice']
        median_sale_20222023 = housing_statistics_json['series']['seriesInfo'][10]['values']['medianSoldPrice']
        median_sale_20212022 = housing_statistics_json['series']['seriesInfo'][9]['values']['medianSoldPrice']
        median_sale_20182019 = housing_statistics_json['series']['seriesInfo'][5]['values']['medianSoldPrice']
        median_sale_20122013 = housing_statistics_json['series']['seriesInfo'][0]['values']['medianSoldPrice']
        appreciation_1yr = round(100.00 * (median_sale_20222023 - median_sale_20212022) / median_sale_20212022, 2)
        appreciation_5yr = round(100.00 * (median_sale_20222023 - median_sale_20182019) / median_sale_20182019, 2)
        appreciation_10yr = round(100.00 * (median_sale_20222023 - median_sale_20122013) / median_sale_20122013, 2)
        suburb_performance_statistics_house.api_calls_made[('House', suburb_performance_statistics_house.data[index]['Suburb'], 
        suburb_performance_statistics_house.data[index]['State'], suburb_performance_statistics_house.data[index]['Postcode'])] = [appreciation_1yr,
        appreciation_5yr, appreciation_10yr, median_annual_rent]
        assert median_annual_rent == 650
        assert appreciation_1yr == -0.28
        assert appreciation_5yr == 13.28
        assert appreciation_10yr == 93.33
        assert suburb_performance_statistics_house.api_calls_made[('House','Hurstville','NSW','2220')] == [appreciation_1yr, appreciation_5yr,
        appreciation_10yr, median_annual_rent]

    def test_apartment_statistics_json(self, apartment_statistics_json, suburb_performance_statistics_apartment, index = 0):
        median_annual_rent = apartment_statistics_json['series']['seriesInfo'][10]['values']['medianRentListingPrice']
        median_sale_20222023 = apartment_statistics_json['series']['seriesInfo'][10]['values']['medianSoldPrice']
        median_sale_20212022 = apartment_statistics_json['series']['seriesInfo'][9]['values']['medianSoldPrice']
        median_sale_20182019 = apartment_statistics_json['series']['seriesInfo'][5]['values']['medianSoldPrice']
        median_sale_20122013 = apartment_statistics_json['series']['seriesInfo'][0]['values']['medianSoldPrice']
        appreciation_1yr = round(100.00 * (median_sale_20222023 - median_sale_20212022) / median_sale_20212022, 2)
        appreciation_5yr = round(100.00 * (median_sale_20222023 - median_sale_20182019) / median_sale_20182019, 2)
        appreciation_10yr = round(100.00 * (median_sale_20222023 - median_sale_20122013) / median_sale_20122013, 2)
        suburb_performance_statistics_apartment.api_calls_made[('Apartment', suburb_performance_statistics_apartment.data[index]['Suburb'], 
        suburb_performance_statistics_apartment.data[index]['State'], suburb_performance_statistics_apartment.data[index]['Postcode'])] = [appreciation_1yr,
        appreciation_5yr, appreciation_10yr, median_annual_rent]
        assert median_annual_rent == 650
        assert appreciation_1yr == 0.0
        assert appreciation_5yr == -2.7
        assert appreciation_10yr == 42.86
        assert suburb_performance_statistics_apartment.api_calls_made[('Apartment','Hurstville','NSW','2220')] == [appreciation_1yr, appreciation_5yr,
        appreciation_10yr, median_annual_rent]

@pytest.fixture
def investor_variable_rate_interest_only():
    investor = Investor()
    investor.loan_type = 'Variable'
    investor.variable_loan_type = 'Interest Only'
    investor.lvr = 80
    investor.loan_term = 10
    investor.mortgage_interest = 3.63
    return investor

@pytest.fixture
def investor_fixed_rate_principal_and_interest():
    investor = Investor()
    investor.loan_type = 'Fixed'
    investor.variable_loan_type = None
    investor.lvr = 80
    investor.loan_term = 2
    investor.mortgage_interest = 4.00
    return investor

@pytest.fixture
def owner_occupier_variable_rate_interest_only():
    owner_occupier = OwnerOccupier()
    owner_occupier.loan_type = 'Variable'
    owner_occupier.variable_loan_type = 'Interest Only'
    owner_occupier.lvr = 80
    owner_occupier.loan_term = 10
    owner_occupier.mortgage_interest = 3.82
    return owner_occupier

@pytest.fixture
def owner_occupier_fixed_rate_principal_and_interest():
    owner_occupier = OwnerOccupier()
    owner_occupier.loan_type = 'Fixed'
    owner_occupier.variable_loan_type = None
    owner_occupier.lvr = 80
    owner_occupier.loan_term = 2
    owner_occupier.mortgage_interest = 3.69
    return owner_occupier

@pytest.fixture
def suburb_performance_statistics_api_calls_house_investor_variable_rate_principal_and_interest(investor, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'House':
        pytest.skip('Metrics calculation for house only')
    residential_listings_search = ResidentialListingsSearch(investor, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(investor, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('House','Hurstville','NSW','2220')] = [10, 50, 80, 800]
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_api_calls_house_investor_variable_rate_interest_only(investor_variable_rate_interest_only, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'House':
        pytest.skip('Metrics calculation for house only')
    residential_listings_search = ResidentialListingsSearch(investor_variable_rate_interest_only, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(investor_variable_rate_interest_only, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('House','Hurstville','NSW','2220')] = [10, 50, 80, 800]
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_api_calls_house_investor_fixed_rate_principal_and_interest(investor_fixed_rate_principal_and_interest, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'House':
        pytest.skip('Metrics calculation for house only')
    residential_listings_search = ResidentialListingsSearch(investor_fixed_rate_principal_and_interest, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(investor_fixed_rate_principal_and_interest, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('House','Hurstville','NSW','2220')] = [10, 50, 80, 800]
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_api_calls_apartment_investor_variable_rate_principal_and_interest(investor, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'Apartment':
        pytest.skip('Metrics calculation for apartment only')
    residential_listings_search = ResidentialListingsSearch(investor, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(investor, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('Apartment','Hurstville','NSW','2220')] = [5, 10, 60, 750]
    return suburb_performance_statistics
@pytest.fixture
def suburb_performance_statistics_api_calls_apartment_investor_variable_rate_interest_only(investor_variable_rate_interest_only, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'Apartment':
        pytest.skip('Metrics calculation for apartment only')
    residential_listings_search = ResidentialListingsSearch(investor_variable_rate_interest_only, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(investor_variable_rate_interest_only, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('Apartment','Hurstville','NSW','2220')] = [5, 10, 60, 750]
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_api_calls_apartment_investor_fixed_rate_principal_and_interest(investor_fixed_rate_principal_and_interest, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'Apartment':
        pytest.skip('Metrics calculation for apartment only')
    residential_listings_search = ResidentialListingsSearch(investor_fixed_rate_principal_and_interest, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(investor_fixed_rate_principal_and_interest, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('Apartment','Hurstville','NSW','2220')] = [5, 10, 60, 750]
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_api_calls_house_owner_occupier_variable_rate_principal_and_interest(owner_occupier, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'House':
        pytest.skip('Metrics calculation for house only')
    residential_listings_search = ResidentialListingsSearch(owner_occupier, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(owner_occupier, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('House','Hurstville','NSW','2220')] = [10, 50, 80, 800]
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_api_calls_house_owner_occupier_variable_rate_interest_only(owner_occupier_variable_rate_interest_only, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'House':
        pytest.skip('Metrics calculation for house only')
    residential_listings_search = ResidentialListingsSearch(owner_occupier_variable_rate_interest_only, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(owner_occupier_variable_rate_interest_only, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('House','Hurstville','NSW','2220')] = [10, 50, 80, 800]
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_api_calls_house_owner_occupier_fixed_rate_principal_and_interest(owner_occupier_fixed_rate_principal_and_interest, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'House':
        pytest.skip('Metrics calculation for house only')
    residential_listings_search = ResidentialListingsSearch(owner_occupier_fixed_rate_principal_and_interest, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(owner_occupier_fixed_rate_principal_and_interest, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('House','Hurstville','NSW','2220')] = [10, 50, 80, 800]
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_api_calls_apartment_owner_occupier_variable_rate_principal_and_interest(owner_occupier, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'Apartment':
        pytest.skip('Metrics calculation for apartment only')
    residential_listings_search = ResidentialListingsSearch(owner_occupier, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(owner_occupier, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('Apartment','Hurstville','NSW','2220')] = [5, 10, 60, 750]
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_api_calls_apartment_owner_occupier_variable_rate_interest_only(owner_occupier_variable_rate_interest_only, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'Apartment':
        pytest.skip('Metrics calculation for apartment only')
    residential_listings_search = ResidentialListingsSearch(owner_occupier_variable_rate_interest_only, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(owner_occupier_variable_rate_interest_only, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('Apartment','Hurstville','NSW','2220')] = [5, 10, 60, 750]
    return suburb_performance_statistics

@pytest.fixture
def suburb_performance_statistics_api_calls_apartment_owner_occupier_fixed_rate_principal_and_interest(owner_occupier_fixed_rate_principal_and_interest, api_client, residential_listings_response):
    if residential_listings_response[0]['listing']['propertyDetails']['propertyType'] != 'Apartment':
        pytest.skip('Metrics calculation for apartment only')
    residential_listings_search = ResidentialListingsSearch(owner_occupier_fixed_rate_principal_and_interest, api_client)
    residential_listings_search.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search)
    property_data.common_listings_data()
    suburb_performance_statistics = SuburbPerformanceStatistics(owner_occupier_fixed_rate_principal_and_interest, api_client, property_data)
    suburb_performance_statistics.api_calls_made[('Apartment','Hurstville','NSW','2220')] = [5, 10, 60, 750]
    return suburb_performance_statistics

class TestMetricsCalculation:
    @pytest.mark.parametrize("suburb_performance_statistics", [
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_house_investor_variable_rate_principal_and_interest'),
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_house_investor_variable_rate_interest_only'),
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_house_investor_fixed_rate_principal_and_interest')
    ])
    def test_calculate_investor_metrics_house(self, suburb_performance_statistics):
        suburb_performance_statistics.calculate_investor_metrics(0, 'House')
        if suburb_performance_statistics.user.loan_type == 'Variable' and suburb_performance_statistics.user.variable_loan_type == 'Principal and Interest':
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'House', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 5.63, 
        'Rental Income' : 3476.19, 'Operating Expenses': 1738.10, 'Cash Flow': 1732.46, 'Cash on Cash Return': 145.38, '1yr Appreciation': 
        10, '5yr Appreciation': 50, '10yr Appreciation': 80}
        elif suburb_performance_statistics.user.loan_type == 'Variable' and suburb_performance_statistics.user.variable_loan_type == 'Interest Only':
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'House', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.73, 
        'Rental Income' : 3476.19, 'Operating Expenses': 1738.10, 'Cash Flow': 1736.36, 'Cash on Cash Return': 145.71, '1yr Appreciation': 
        10, '5yr Appreciation': 50, '10yr Appreciation': 80}
        else:
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'House', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 24.84, 
        'Rental Income' : 3476.19, 'Operating Expenses': 1738.10, 'Cash Flow': 1713.25, 'Cash on Cash Return': 143.77, '1yr Appreciation': 
        10, '5yr Appreciation': 50, '10yr Appreciation': 80}
    
    @pytest.mark.parametrize("suburb_performance_statistics", [
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_apartment_investor_variable_rate_principal_and_interest'),
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_apartment_investor_variable_rate_interest_only'),
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_apartment_investor_fixed_rate_principal_and_interest')
    ])
    def test_calculate_investor_metrics_apartment(self, suburb_performance_statistics):
        suburb_performance_statistics.calculate_investor_metrics(0, 'Apartment')
        if suburb_performance_statistics.user.loan_type == 'Variable' and suburb_performance_statistics.user.variable_loan_type == 'Principal and Interest':
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'Apartment', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 5.63, 
        'Rental Income' : 3258.93, 'Operating Expenses': 1629.46, 'Cash Flow': 1623.84, 'Cash on Cash Return': 136.27, '1yr Appreciation': 
        5, '5yr Appreciation': 10, '10yr Appreciation': 60}
        elif suburb_performance_statistics.user.loan_type == 'Variable' and suburb_performance_statistics.user.variable_loan_type == 'Interest Only':
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'Apartment', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.73, 
        'Rental Income' : 3258.93, 'Operating Expenses': 1629.46, 'Cash Flow': 1627.74, 'Cash on Cash Return': 136.59, '1yr Appreciation': 
        5, '5yr Appreciation': 10, '10yr Appreciation': 60}
        else:
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'Apartment', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 24.84, 
        'Rental Income' : 3258.93, 'Operating Expenses': 1629.46, 'Cash Flow': 1604.63, 'Cash on Cash Return': 134.65, '1yr Appreciation': 
        5, '5yr Appreciation': 10, '10yr Appreciation': 60}
    
    @pytest.mark.parametrize("suburb_performance_statistics", [
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_house_owner_occupier_variable_rate_principal_and_interest'),
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_house_owner_occupier_variable_rate_principal_and_interest'),
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_house_owner_occupier_variable_rate_principal_and_interest')
    ])
    def test_calculate_owner_occupier_metrics_house(self, suburb_performance_statistics):
        suburb_performance_statistics.calculate_owner_occupier_metrics(0, 'House')
        if suburb_performance_statistics.user.loan_type == 'Variable' and suburb_performance_statistics.user.variable_loan_type == 'Principal and Interest':
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'House', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 5.54, 
        '10yr Appreciation': 80}
        elif suburb_performance_statistics.user.loan_type == 'Variable' and suburb_performance_statistics.user.variable_loan_type == 'Interest Only':
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.82,  
        '10yr Appreciation': 80}
        else:
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 24.76, 
        '10yr Appreciation': 80}
    
    @pytest.mark.parametrize("suburb_performance_statistics", [
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_apartment_owner_occupier_variable_rate_principal_and_interest'),
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_apartment_owner_occupier_variable_rate_interest_only'),
        pytest.lazy_fixture('suburb_performance_statistics_api_calls_apartment_owner_occupier_fixed_rate_principal_and_interest')
    ])
    def test_calculate_owner_occupier_metrics_apartment(self, suburb_performance_statistics):
        suburb_performance_statistics.calculate_owner_occupier_metrics(0, 'Apartment')
        if suburb_performance_statistics.user.loan_type == 'Variable' and suburb_performance_statistics.user.variable_loan_type == 'Principal and Interest':
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'Apartment', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 5.54, 
        '10yr Appreciation': 60}
        elif suburb_performance_statistics.user.loan_type == 'Variable' and suburb_performance_statistics.user.variable_loan_type == 'Interest Only':
            assert suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'Apartment', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.82, 
        '10yr Appreciation': 60}
        else:
            suburb_performance_statistics.data[0] == {'Listing Date': '2022-07-05', 'Property Type': 'Apartment', 'Suburb': 'Hurstville', 'State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 24.76, 
        '10yr Appreciation': 60}

@pytest.fixture
def renter_customer_email(residential_listings_search_renter, residential_listings_response):
    residential_listings_search_renter.responses.append(residential_listings_response)
    property_data = PropertyData(residential_listings_search_renter)
    property_data.common_listings_data()
    property_data.listings_data_rent()
    customer_email = CustomerEmail(property_data = property_data)
    return customer_email

@pytest.fixture
def investor_customer_email(suburb_performance_statistics_api_calls_house_investor_variable_rate_principal_and_interest):
    suburb_performance_statistics_api_calls_house_investor_variable_rate_principal_and_interest.calculate_investor_metrics(0, 'House')
    customer_email = CustomerEmail(suburb_performance_statistics = suburb_performance_statistics_api_calls_house_investor_variable_rate_principal_and_interest)
    return customer_email

@pytest.fixture
def owner_occupier_customer_email(suburb_performance_statistics_api_calls_house_owner_occupier_variable_rate_principal_and_interest):
    suburb_performance_statistics_api_calls_house_owner_occupier_variable_rate_principal_and_interest.calculate_owner_occupier_metrics(0, 'House')
    customer_email = CustomerEmail(suburb_performance_statistics = suburb_performance_statistics_api_calls_house_owner_occupier_variable_rate_principal_and_interest)
    return customer_email

class TestCustomerEmail:
    smtp_servers=['smtp.gmail.com', 'smtp.office365.com']

    @pytest.mark.parametrize('email_object', [pytest.lazy_fixture('renter_customer_email'),
    pytest.lazy_fixture('investor_customer_email'),
    pytest.lazy_fixture('owner_occupier_customer_email')])
    def test_create_csv_attachment(self, email_object):
        email_object.create_csv_attachment()
        assert email_object.data_io != None

    @pytest.mark.parametrize('email_object, smtp_servers', [(pytest.lazy_fixture('renter_customer_email'), smtp_servers)])
    def test_send_email_renter(self, email_object, smtp_servers, mocker):
        smtp_mock = mocker.MagicMock()
        mocker.patch('property_notifier.smtplib.SMTP', new = smtp_mock)
        email_object.create_csv_attachment()
        email_object.send_email_renter(smtp_servers)
        smtp_mock.assert_called_once_with(smtp_servers,587)

    @pytest.mark.parametrize('email_object, smtp_servers', [(pytest.lazy_fixture('investor_customer_email'), smtp_servers),
    (pytest.lazy_fixture('owner_occupier_customer_email'), smtp_servers)])
    def test_send_email_investor_owner_occupier(self, email_object, smtp_servers, mocker):
        smtp_mock = mocker.MagicMock()
        mocker.patch('property_notifier.smtplib.SMTP', new = smtp_mock)
        email_object.create_csv_attachment()
        email_object.send_email_renter(smtp_servers)
        smtp_mock.assert_called_once_with(smtp_servers,587)



