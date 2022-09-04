import pytest
import property_notifier
import requests
import requests_mock
import json
import pytest_mock

class Test_Mortgage_Interest_Functions_Investor:
    def test_investor_fixed_rate_loan_term_2yr(self):
        investor=property_notifier.Investor()
        investor.loan_type='Fixed'
        investor.variable_loan_type=None
        investor.lvr=80
        investor.loan_term=2
        investor.fixed_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 4.00

    def test_investor_fixed_rate_loan_term_5yr(self):
        investor=property_notifier.Investor()
        investor.loan_type='Fixed'
        investor.variable_loan_type=None
        investor.lvr=80
        investor.loan_term=5
        investor.fixed_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 4.73
    
    def test_investor_variable_rate_principal_and_interest_lvr_80_loan_term_10yr(self):
        investor=property_notifier.Investor()
        investor.loan_type='Variable'
        investor.variable_loan_type='Principal and Interest'
        investor.lvr=80
        investor.loan_term=10
        investor.variable_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 3.42
    
    def test_investor_variable_rate_principal_and_interest_lvr_90_loan_term_10yr(self):
        investor=property_notifier.Investor()
        investor.loan_type='Variable'
        investor.variable_loan_type='Principal and Interest'
        investor.lvr=90
        investor.loan_term=10
        investor.variable_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 3.72
    
    def test_investor_variable_rate_interest_only_lvr_80_loan_term_10yr(self):
        investor=property_notifier.Investor()
        investor.loan_type='Variable'
        investor.variable_loan_type='Interest Only'
        investor.lvr=80
        investor.loan_term=10
        investor.variable_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 3.63
    
    def test_investor_variable_rate_interest_only_lvr_90_loan_term_10yr(self):
        investor=property_notifier.Investor()
        investor.loan_type='Vairable'
        investor.variable_loan_type='Interest Only'
        investor.lvr=90
        investor.loan_term=10
        investor.variable_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 3.93

class Test_Mortgage_Interest_Functions_Owner_Occupier:
    def test_owner_occupier_fixed_rate_loan_term_2yr(self):
        owner_occupier=property_notifier.Owner_Occupier()
        owner_occupier.loan_type='Fixed'
        owner_occupier.variable_loan_type=None
        owner_occupier.lvr=80
        owner_occupier.loan_term=2
        owner_occupier.fixed_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 3.69

    def test_owner_occupier_fixed_rate_loan_term_5yr(self):
        owner_occupier=property_notifier.Owner_Occupier()
        owner_occupier.loan_type='Fixed'
        owner_occupier.variable_loan_type=None
        owner_occupier.lvr=80
        owner_occupier.loan_term=5
        owner_occupier.fixed_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 4.54
    
    def test_owner_occupier_variable_rate_principal_and_interest_lvr_80_loan_term_10yr(self):
        owner_occupier=property_notifier.Owner_Occupier()
        owner_occupier.loan_type='Variable'
        owner_occupier.variable_loan_type='Principal and Interest'
        owner_occupier.lvr=80
        owner_occupier.loan_term=10
        owner_occupier.variable_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 3.07
    
    def test_owner_occupier_variable_rate_principal_and_interest_lvr_90_loan_term_10yr(self):
        owner_occupier=property_notifier.Owner_Occupier()
        owner_occupier.loan_type='Variable'
        owner_occupier.variable_loan_type='Principal and Interest'
        owner_occupier.lvr=90
        owner_occupier.loan_term=10
        owner_occupier.variable_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 3.37
    
    def test_owner_occupier_variable_rate_interest_only_lvr_80_loan_term_10yr(self):
        owner_occupier=property_notifier.Owner_Occupier()
        owner_occupier.loan_type='Variable'
        owner_occupier.variable_loan_type='Interest Only'
        owner_occupier.lvr=80
        owner_occupier.loan_term=10
        owner_occupier.variable_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 3.82
    
    def test_owner_occupier_variable_rate_interest_only_lvr_90_loan_term_10yr(self):
        owner_occupier=property_notifier.Owner_Occupier()
        owner_occupier.loan_type='Variable'
        owner_occupier.variable_loan_type='Interest Only'
        owner_occupier.lvr=90
        owner_occupier.loan_term=10
        owner_occupier.variable_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 4.12

class Test_Access_Token:
    def test_connection(self):
        api=property_notifier.API()
        with requests_mock.mock() as m:
            m.post('https://auth.domain.com.au/v1/connect/token',json={'access_token':'token','expires_in':43200,'token_type':'Bearer'})
            response=requests.post('https://auth.domain.com.au/v1/connect/token',data={'client_id':api.client_id,
            'client_secret':api.client_secret,'grant_type':'client_credentials','scope':api.scopes, 'Content-Type':'text/json'})
            assert response.json()['access_token'] == 'token'

@pytest.fixture
def renter():
    renter=property_notifier.Renter()
    renter.locations=[{'Hurstville':'NSW'},{'Penshurst':'NSW'}]
    renter.property_types=['House','Apartment']
    renter.bedrooms=3
    renter.bathrooms=2
    renter.car_spaces=2
    renter.date_posted='2022-06-17'
    renter.min_price=500
    renter.max_price=800
    return renter

@pytest.fixture
def investor():
    investor=property_notifier.Investor()
    investor.locations=[{'Hurstville':'NSW'},{'Penshurst':'NSW'}]
    investor.property_types=['House','Apartment']
    investor.bedrooms=3
    investor.bathrooms=2
    investor.car_spaces=2
    investor.date_posted='2022-06-17'
    investor.min_price=500
    investor.max_price=800
    investor.loan_type='Variable'
    investor.variable_loan_type='Principal and Interest'
    investor.lvr=80
    investor.loan_term=10
    investor.mortgage_interest=3.42
    return investor

@pytest.fixture
def owner_occupier():
    owner_occupier=property_notifier.Owner_Occupier()
    owner_occupier.locations=[{'Hurstville':'NSW'},{'Penshurst':'NSW'}]
    owner_occupier.property_types=['House','Apartment']
    owner_occupier.bedrooms=3
    owner_occupier.bathrooms=2
    owner_occupier.car_spaces=2
    owner_occupier.date_posted='2022-06-17'
    owner_occupier.min_price=500
    owner_occupier.max_price=800
    owner_occupier.loan_type='Variable'
    owner_occupier.variable_loan_type='Principal and Interest'
    owner_occupier.lvr=80
    owner_occupier.loan_term=10
    owner_occupier.mortgage_interest=3.07
    return owner_occupier

@pytest.fixture
def access_token():
    api=property_notifier.API()
    with requests_mock.mock() as m:
        m.post('https://auth.domain.com.au/v1/connect/token',json={'access_token':'token','expires_in':43200,'token_type':'Bearer'})
        response=requests.post('https://auth.domain.com.au/v1/connect/token',data={'client_id':api.client_id,
        'client_secret':api.client_secret,'grant_type':'client_credentials','scope':api.scopes, 'Content-Type':'text/json'})
        return response.json()['access_token']

class Test_Listings_Request:    
    def test_listings_request_renter(self,renter,access_token):
        for location in renter.locations:
            for suburb,state in location.items():
                with requests_mock.mock() as m:
                    m.post('https://api.domain.com.au/v1/listings/residential/_search',json=[{'type':"PropertyListing",
                    "listing":{"listingType":"Rent"}}])
                    response=requests.post('https://api.domain.com.au/v1/listings/residential/_search',json={
                        'listingType':'Rent' if isinstance(renter,property_notifier.Renter) else 'Sale',
                        'propertyTypes':renter.property_types,
                        'minBedrooms':renter.bedrooms,
                        'minBathrooms':renter.bathrooms,
                        'minCarspaces':renter.car_spaces,
                        'minPrice':renter.min_price,
                        'maxPrice':renter.max_price,
                        'locations':[
                            {
                                'state':state,
                                'region': '',
                                'area': '',
                                'suburb': suburb,
                                'postcode': '',
                                'includeSurroundingSuburbs': False
                            }
                        ],
                        'excludePriceWithheld': False,
                        'excludeDepositTaken': True,
                        'pageSize':50,
                        'listedSince':f'{renter.date_posted}'},headers={'Authorization':'Bearer '+ access_token})
                    assert response.json() == [{'type':"PropertyListing","listing":{"listingType":"Rent"}}]

    @pytest.mark.parametrize('user_type',[pytest.lazy_fixture('investor'),pytest.lazy_fixture('owner_occupier')])
    def test_listings_request_nonrenter(self,user_type,access_token):
        for location in user_type.locations:
            for suburb,state in location.items():
                with requests_mock.mock() as m:
                    m.post('https://api.domain.com.au/v1/listings/residential/_search',json=[{'type':"PropertyListing",
                    "listing":{"listingType":"Sale"}}])
                    response=requests.post('https://api.domain.com.au/v1/listings/residential/_search',json={
                        'listingType':'Rent' if isinstance(user_type,property_notifier.Renter) else 'Sale',
                        'propertyTypes':user_type.property_types,
                        'minBedrooms':user_type.bedrooms,
                        'minBathrooms':user_type.bathrooms,
                        'minCarspaces':user_type.car_spaces,
                        'minPrice':user_type.min_price,
                        'maxPrice':user_type.max_price,
                        'locations':[
                            {
                                'state':state,
                                'region': '',
                                'area': '',
                                'suburb': suburb,
                                'postcode': '',
                                'includeSurroundingSuburbs': False
                            }
                        ],
                        'excludePriceWithheld': False,
                        'excludeDepositTaken': True,
                        'pageSize':50,
                        'listedSince':f'{user_type.date_posted}'},headers={'Authorization':'Bearer '+ access_token})
                    assert response.json() == [{'type':"PropertyListing","listing":{"listingType":"Sale"}}]

@pytest.fixture(params=["Sale","Rent"])
def listings_response(request):
    residential_listings_search=property_notifier.Residential_Listings_Search()
    residential_listings_search.responses.append(
  [
  {
    "type": "PropertyListing",
    "listing": {
      "listingType": request.param,
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
        "propertyType": "House",
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
  }])
    return residential_listings_search

@pytest.fixture
def property_data():
    property_data=property_notifier.property_data
    yield property_data
    property_data.clear()

@pytest.mark.parametrize('user_type',[pytest.lazy_fixture('investor'),pytest.lazy_fixture('renter'),pytest.lazy_fixture('owner_occupier')])
def test_common_listings_data(user_type,property_data,listings_response):
    property_notifier.common_listings_data(user_type,property_data,listings_response)
    assert property_data[0] == {'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
    'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
    'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998'}

@pytest.fixture
def property_data_withinput_house(property_data):
    property_data.append({'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
    'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
    'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998'})
    return property_data

@pytest.fixture
def property_data_withinput_apartment(property_data):
    property_data.append({'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
    'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
    'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998'})
    return property_data

class Test_Listings_Data:
    def test_listings_data_rent(self,property_data_withinput_house):
        property_notifier.listings_data_rent(property_data_withinput_house)
        assert property_data_withinput_house[0] == {'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A',
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Weekly Rent': 715.00, 'Annual Rent': 37180.00}

    def test_listings_data_sale(self,property_data_withinput_house):
        property_notifier.listings_data_sale(property_data_withinput_house)
        assert property_data_withinput_house[0] == {'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715000.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998'}

class Test_Listings_Request:
    def test_house_request_json(self,investor,access_token,property_data_withinput_house):
        with requests_mock.mock() as m:
            m.get('https://api.domain.com.au/v2/suburbPerformanceStatistics/NSW/Hurstville/2220?propertyCategory=House&bedrooms=3&periodSize=Years&startingPeriodRelativeToCurrent=1&totalPeriods=11',
            json={'header': {'suburb':property_data_withinput_house[0]['Suburb'],
            'state':property_data_withinput_house[0]['State'], 'property_category': 'House'}})
            response=requests.get('https://api.domain.com.au/v2/suburbPerformanceStatistics/' + property_data_withinput_house[0]['State'] + '/' 
            + property_data_withinput_house[0]['Suburb'].replace(' ','%20')+ '/' + property_data_withinput_house[0]['Postcode'] + '?' 
            + f'propertyCategory=House' 
            + '&' + f'bedrooms={investor.bedrooms}'+ '&' + 'periodSize=years' + '&' + 'startingPeriodRelativeToCurrent=1' + '&' 
            + 'totalPeriods=11', headers={'Authorization':'Bearer ' + access_token})
            assert response.json() == {'header': {'suburb':property_data_withinput_house[0]['Suburb'],
            'state':property_data_withinput_house[0]['State'], 'property_category': 'House'}}

    def test_apartment_request_json(self,investor,access_token,property_data_withinput_apartment):
        with requests_mock.mock() as m:
            m.get('https://api.domain.com.au/v2/suburbPerformanceStatistics/NSW/Hurstville/2220?propertyCategory=Unit&bedrooms=3&periodSize=Years&startingPeriodRelativeToCurrent=1&totalPeriods=11',
            json={'header': {'suburb':property_data_withinput_apartment[0]['Suburb'],
            'state':property_data_withinput_apartment[0]['State'], 'property_category': 'Unit'}})
            response=requests.get('https://api.domain.com.au/v2/suburbPerformanceStatistics/' + property_data_withinput_apartment[0]['State'] + '/' 
            + property_data_withinput_apartment[0]['Suburb'].replace(' ','%20')+ '/' + property_data_withinput_apartment[0]['Postcode'] + '?' 
            + 'propertyCategory=Unit' 
            + '&' + f'bedrooms={investor.bedrooms}'+ '&' + 'periodSize=years' + '&' + 'startingPeriodRelativeToCurrent=1' + '&' 
            + 'totalPeriods=11', headers={'Authorization':'Bearer ' + access_token})
            assert response.json() == {'header': {'suburb':property_data_withinput_apartment[0]['Suburb'],
            'state':property_data_withinput_apartment[0]['State'], 'property_category': 'Unit'}}

@pytest.fixture
def housing_statistics_json():
    house_stats_file=open(r"C:\Users\kpali\Downloads\house_stats_json_testsample.json")
    return json.loads(house_stats_file.read())

@pytest.fixture
def apartment_statistics_json():
    apartment_stats_file=open(r"C:\Users\kpali\Downloads\unit_apartment_stats_json_testsample.json")
    return json.loads(apartment_stats_file.read())

class Test_Statistics_Request:
    def test_house_statistics_json(self,housing_statistics_json,property_data_withinput_house,index=0):
        suburb_performance_statistics=property_notifier.Suburb_Performance_Statistics()
        house_stats=housing_statistics_json
        median_annual_rent=house_stats['series']['seriesInfo'][0]['values']['medianRentListingPrice']
        median_sale_20212022=house_stats['series']['seriesInfo'][10]['values']['medianSoldPrice']
        median_sale_20202021=house_stats['series']['seriesInfo'][9]['values']['medianSoldPrice']
        median_sale_20172018=house_stats['series']['seriesInfo'][5]['values']['medianSoldPrice']
        median_sale_20112012=house_stats['series']['seriesInfo'][0]['values']['medianSoldPrice']
        appreciation_1yr=round(100.00*(median_sale_20212022-median_sale_20202021)/median_sale_20202021,2)
        appreciation_5yr=round(100.00*(median_sale_20212022-median_sale_20172018)/median_sale_20172018,2)
        appreciation_10yr=round(100.00*(median_sale_20212022-median_sale_20112012)/median_sale_20112012,2)
        suburb_performance_statistics.api_calls_made[('House',property_data_withinput_house[index]['Suburb'],property_data_withinput_house[index]['State'],property_data_withinput_house[index]['Postcode'])]=[appreciation_1yr,
        appreciation_5yr,appreciation_10yr,median_annual_rent]
        assert suburb_performance_statistics.api_calls_made[('House','Hurstville','NSW','2220')] == [appreciation_1yr,appreciation_5yr,
        appreciation_10yr,median_annual_rent]

    def test_apartment_statistics_json(self,apartment_statistics_json,property_data_withinput_apartment,index=0):
        suburb_performance_statistics=property_notifier.Suburb_Performance_Statistics()
        apartment_stats=apartment_statistics_json
        median_annual_rent=apartment_stats['series']['seriesInfo'][0]['values']['medianRentListingPrice']
        median_sale_20212022=apartment_stats['series']['seriesInfo'][10]['values']['medianSoldPrice']
        median_sale_20202021=apartment_stats['series']['seriesInfo'][9]['values']['medianSoldPrice']
        median_sale_20172018=apartment_stats['series']['seriesInfo'][5]['values']['medianSoldPrice']
        median_sale_20112012=apartment_stats['series']['seriesInfo'][0]['values']['medianSoldPrice']
        appreciation_1yr=round(100.00*(median_sale_20212022-median_sale_20202021)/median_sale_20202021,2)
        appreciation_5yr=round(100.00*(median_sale_20212022-median_sale_20172018)/median_sale_20172018,2)
        appreciation_10yr=round(100.00*(median_sale_20212022-median_sale_20112012)/median_sale_20112012,2)
        suburb_performance_statistics.api_calls_made[('Apartment',property_data_withinput_apartment[index]['Suburb'],property_data_withinput_apartment[index]['State'],property_data_withinput_apartment[index]['Postcode'])]=[appreciation_1yr,
        appreciation_5yr,appreciation_10yr,median_annual_rent]
        assert suburb_performance_statistics.api_calls_made[('Apartment','Hurstville','NSW','2220')] == [appreciation_1yr,appreciation_5yr,
        appreciation_10yr,median_annual_rent]

@pytest.fixture
def suburb_performance_statistics_api_calls_house():
    suburb_performance_statistics=property_notifier.Suburb_Performance_Statistics()
    suburb_performance_statistics.api_calls_made[('House','Hurstville','NSW','2220')] = [10,50,80,800]
    yield suburb_performance_statistics
    suburb_performance_statistics.api_calls_made.clear()

@pytest.fixture
def suburb_performance_statistics_api_calls_apartment():
    suburb_performance_statistics=property_notifier.Suburb_Performance_Statistics()
    suburb_performance_statistics.api_calls_made[('Apartment','Hurstville','NSW','2220')] = [5,10,60,750]
    yield suburb_performance_statistics
    suburb_performance_statistics.api_calls_made.clear()

@pytest.fixture
def investor_variable_rate_interest_only():
    investor=property_notifier.Investor()
    investor.loan_type='Variable'
    investor.variable_loan_type='Interest Only'
    investor.lvr=80
    investor.loan_term=10
    investor.mortgage_interest=3.63
    return investor

@pytest.fixture
def investor_fixed_rate_principal_and_interest():
    investor=property_notifier.Investor()
    investor.loan_type='Fixed'
    investor.variable_loan_type=None
    investor.lvr=80
    investor.loan_term=2
    investor.mortgage_interest=4.00
    return investor

@pytest.fixture
def owner_occupier_variable_rate_interest_only():
    owner_occupier=property_notifier.Owner_Occupier()
    owner_occupier.loan_type='Variable'
    owner_occupier.variable_loan_type='Interest Only'
    owner_occupier.lvr=80
    owner_occupier.loan_term=10
    owner_occupier.mortgage_interest=3.82
    return owner_occupier

@pytest.fixture
def owner_occupier_fixed_rate_principal_and_interest():
    owner_occupier=property_notifier.Owner_Occupier()
    owner_occupier.loan_type='Fixed'
    owner_occupier.variable_loan_type=None
    owner_occupier.lvr=80
    owner_occupier.loan_term=2
    owner_occupier.mortgage_interest=3.69
    return owner_occupier

class Test_Property_Calculations_Investor:
    def test_investor_calculation_house_data_interest_only(self,investor_variable_rate_interest_only,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.investor_calculation_house_data(investor_variable_rate_interest_only,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.73, 
        'Rental Income' : 3476.19, 'Operating Expenses': 1738.10, 'Cash Flow': 1736.36, 'Cash on Cash Return': 145.71, '1yr Appreciation': 
        10, '5yr Appreciation': 50, '10yr Appreciation': 80}
    
    def test_investor_calculation_house_data_principal_and_interest(self,investor,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.investor_calculation_house_data(investor,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 5.63, 
        'Rental Income' : 3476.19, 'Operating Expenses': 1738.10, 'Cash Flow': 1732.46, 'Cash on Cash Return': 145.38, '1yr Appreciation': 
        10, '5yr Appreciation': 50, '10yr Appreciation': 80}
    
    def test_investor_calculation_house_data_fixed_rate(self,investor_fixed_rate_principal_and_interest,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.investor_calculation_house_data(investor_fixed_rate_principal_and_interest,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 24.84, 
        'Rental Income' : 3476.19, 'Operating Expenses': 1738.10, 'Cash Flow': 1713.25, 'Cash on Cash Return': 143.77, '1yr Appreciation': 
        10, '5yr Appreciation': 50, '10yr Appreciation': 80}
    
    def test_investor_calculation_apartment_data_interest_only(self,investor_variable_rate_interest_only,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.investor_calculation_apartment_data(investor_variable_rate_interest_only,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.73, 
        'Rental Income' : 3258.93, 'Operating Expenses': 1629.46, 'Cash Flow': 1627.74, 'Cash on Cash Return': 136.59, '1yr Appreciation': 
        5, '5yr Appreciation': 10, '10yr Appreciation': 60}
    
    def test_investor_calculation_apartment_data_principal_and_interest(self,investor,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.investor_calculation_apartment_data(investor,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 5.63, 
        'Rental Income' : 3258.93, 'Operating Expenses': 1629.46, 'Cash Flow': 1623.84, 'Cash on Cash Return': 136.27, '1yr Appreciation': 
        5, '5yr Appreciation': 10, '10yr Appreciation': 60}
    
    def test_investor_calculation_apartment_data_fixed_rate(self,investor_fixed_rate_principal_and_interest,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.investor_calculation_apartment_data(investor_fixed_rate_principal_and_interest,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 24.84, 
        'Rental Income' : 3258.93, 'Operating Expenses': 1629.46, 'Cash Flow': 1604.63, 'Cash on Cash Return': 134.65, '1yr Appreciation': 
        5, '5yr Appreciation': 10, '10yr Appreciation': 60}
    
class Test_Property_Calculations_Owner_Occupier:
    def test_owner_occupier_calculation_house_data_interest_only(self,owner_occupier_variable_rate_interest_only,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.owner_occupier_calculation_house_data(owner_occupier_variable_rate_interest_only,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.82,  
        '10yr Appreciation': 80}

    def test_owner_occupier_calculation_house_data_principal_and_interest(self,owner_occupier,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.owner_occupier_calculation_house_data(owner_occupier,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 5.54, 
        '10yr Appreciation': 80}
    
    def test_owner_occupier_calculation_house_data_fixed_rate(self,owner_occupier_fixed_rate_principal_and_interest,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.owner_occupier_calculation_house_data(owner_occupier_fixed_rate_principal_and_interest,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 24.76, 
        '10yr Appreciation': 80}

    def test_owner_occupier_calculation_apartment_data_interest_only(self,owner_occupier_variable_rate_interest_only,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.owner_occupier_calculation_apartment_data(owner_occupier_variable_rate_interest_only,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.82, 
        '10yr Appreciation': 60}

    def test_owner_occupier_calculation_apartment_data_principal_and_interest(self,owner_occupier,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.owner_occupier_calculation_apartment_data(owner_occupier,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 5.54, 
        '10yr Appreciation': 60}
    
    def test_owner_occupier_calculation_apartment_data_fixed_rate(self,owner_occupier_fixed_rate_principal_and_interest,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.owner_occupier_calculation_apartment_data(owner_occupier_fixed_rate_principal_and_interest,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 24.76, 
        '10yr Appreciation': 60}

@pytest.fixture
def renter_house_property_data_with_calculations(property_data):
    property_data.append({'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
    'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A','Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 
    'Weekly Rent': 715.00, 'Annual Rent': 37180.00})
    return property_data

@pytest.fixture
def investor_house_property_data_with_calculations(property_data):
    property_data.append({'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
    'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
    'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998','Mortgage Repayments': 10.56, 
    'Rental Income' : 750, 'Operating Expenses': 375.00, 'Cash Flow': 364.44, 'Cash on Cash Return': 30.58, 
    '1yr Appreciation': 5, '5yr Appreciation': 10, '10yr Appreciation': 60})
    return property_data

@pytest.fixture
def owner_occupier_house_property_data_with_calculations(property_data):
    property_data.append({'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
    'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
    'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 10.49, 
    '10yr Appreciation': 60})
    return property_data

@pytest.fixture
def customer_email():
    customer_email=property_notifier.Customer_Email()
    return customer_email

class Test_CSV_Attachment:
    @pytest.mark.parametrize('sample_data',[pytest.lazy_fixture('renter_house_property_data_with_calculations'),
    pytest.lazy_fixture('investor_house_property_data_with_calculations'),
    pytest.lazy_fixture('owner_occupier_house_property_data_with_calculations')])
    def test_create_csv_attachment(self,sample_data,customer_email):
        customer_email.create_csv_attachment(sample_data)
        assert customer_email.property_data_io!=None

class Test_Sending_Emails:
    smtp_servers=['smtp.gmail.com','smtp.office365.com']

    @pytest.mark.parametrize('smtp_servers',smtp_servers)
    def test_send_email_renter(self,customer_email,renter_house_property_data_with_calculations,renter,smtp_servers,mocker):
        smtp_mock=mocker.MagicMock()
        mocker.patch('property_notifier.smtplib.SMTP',new=smtp_mock)
        customer_email.create_csv_attachment(renter_house_property_data_with_calculations)
        customer_email.send_email_renter(renter,smtp_servers)
        smtp_mock.assert_called_once_with(smtp_servers,587)

    @pytest.mark.parametrize('smtp_servers',smtp_servers)
    def test_send_email_investor_owner_occupier_investor(self,customer_email,investor_house_property_data_with_calculations,investor,smtp_servers,mocker):
        smtp_mock=mocker.MagicMock()
        mocker.patch('property_notifier.smtplib.SMTP',new=smtp_mock)
        customer_email.create_csv_attachment(investor_house_property_data_with_calculations)
        customer_email.send_email_renter(investor,smtp_servers)
        smtp_mock.assert_called_once_with(smtp_servers,587)
    
    @pytest.mark.parametrize('smtp_servers',smtp_servers)
    def test_send_email_investor_owner_occupier_owner_occupier(self,customer_email,owner_occupier_house_property_data_with_calculations,owner_occupier,smtp_servers,mocker):
        smtp_mock=mocker.MagicMock()
        mocker.patch('property_notifier.smtplib.SMTP',new=smtp_mock)
        customer_email.create_csv_attachment(owner_occupier_house_property_data_with_calculations)
        customer_email.send_email_renter(owner_occupier,smtp_servers)
        smtp_mock.assert_called_once_with(smtp_servers,587)



