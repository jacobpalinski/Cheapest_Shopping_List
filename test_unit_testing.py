import pytest
import property_notifier
import requests
import requests_mock
import json

class Test_Prompts:
    def test_renter_prompt(self,monkeypatch):
        renter=property_notifier.Renter()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        renter.prompt()
        assert renter.__dict__ == {'locations': [{'Madeley':'WA'},{'Darch':'WA'},{'Two Rocks':'WA'}], 
        'property_types':['House', 'ApartmentUnitFlat'],'bedrooms':3,'bathrooms':2, 'car_spaces':2,
        'date_posted': '2022-06-17', 'car_spaces':2, 'min_price':300, 'max_price':600}

    def test_owner_occupier_variable_rate_principal_and_interest_lvr80_prompt(self,monkeypatch):
        owner_occupier=property_notifier.Owner_Occupier()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600',
        'Variable','Principal and Interest','80']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        owner_occupier.prompt()
        assert owner_occupier.__dict__ == {'locations': [{'Madeley':'WA'},{'Darch':'WA'},{'Two Rocks':'WA'}], 
        'property_types':['House', 'ApartmentUnitFlat'],'bedrooms':3,'bathrooms':2, 'car_spaces':2,
        'date_posted': '2022-06-17', 'car_spaces':2, 'min_price':300, 'max_price':600,'loan_type':'Variable',
        'variable_loan_type':'Principal And Interest','lvr':80, 'loan_term':None, 'mortgage_interest':None}
    
    def test_owner_occupier_variable_rate_interest_only_lvr80_prompt(self,monkeypatch):
        owner_occupier=property_notifier.Owner_Occupier()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600',
        'Variable','Interest Only','80']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        owner_occupier.prompt()
        assert owner_occupier.__dict__ == {'locations': [{'Madeley':'WA'},{'Darch':'WA'},{'Two Rocks':'WA'}], 
        'property_types':['House', 'ApartmentUnitFlat'],'bedrooms':3,'bathrooms':2, 'car_spaces':2,
        'date_posted': '2022-06-17', 'car_spaces':2, 'min_price':300, 'max_price':600,'loan_type':'Variable',
        'variable_loan_type':'Interest Only','lvr':80, 'loan_term':None, 'mortgage_interest':None}
    
    def test_owner_occupier_fixed_rate_lvr80_prompt(self,monkeypatch):
        owner_occupier=property_notifier.Owner_Occupier()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','fixed',
        '80']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        owner_occupier.prompt()
        assert owner_occupier.__dict__ == {'locations': [{'Madeley':'WA'},{'Darch':'WA'},{'Two Rocks':'WA'}], 
        'property_types':['House', 'ApartmentUnitFlat'],'bedrooms':3,'bathrooms':2, 'car_spaces':2,
        'date_posted': '2022-06-17', 'car_spaces':2, 'min_price':300, 'max_price':600,'loan_type':'Fixed',
        'variable_loan_type': None,'lvr':80, 'loan_term':None, 'mortgage_interest':None}
    
    def test_investor_variable_rate_lvr80_prompt(self,monkeypatch):
        investor=property_notifier.Investor()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','Variable',
        'Principal and Interest','80']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        investor.prompt()
        assert investor.__dict__ == {'locations': [{'Madeley':'WA'},{'Darch':'WA'},{'Two Rocks':'WA'}], 
        'property_types':['House', 'ApartmentUnitFlat'],'bedrooms':3,'bathrooms':2, 'car_spaces':2,
        'date_posted': '2022-06-17', 'car_spaces':2, 'min_price':300, 'max_price':600,'loan_type':'Variable',
        'variable_loan_type':'Principal And Interest','lvr':80, 'loan_term':None, 'mortgage_interest':None}
    
    def test_investor_fixed_rate_lvr80_prompt(self,monkeypatch):
        investor=property_notifier.Investor()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','fixed',
        '80']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        investor.prompt()
        assert investor.__dict__ == {'locations': [{'Madeley':'WA'},{'Darch':'WA'},{'Two Rocks':'WA'}], 
        'property_types':['House', 'ApartmentUnitFlat'],'bedrooms':3,'bathrooms':2, 'car_spaces':2,
        'date_posted': '2022-06-17', 'car_spaces':2, 'min_price':300, 'max_price':600,'loan_type':'Fixed',
        'variable_loan_type': None,'lvr':80, 'loan_term':None, 'mortgage_interest':None}
    
    def test_investor_variable_rate_interest_only_lvr80_prompt(self,monkeypatch):
        investor=property_notifier.Investor()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600',
        'Variable','Interest Only','80']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        investor.prompt()
        assert investor.__dict__ == {'locations': [{'Madeley':'WA'},{'Darch':'WA'},{'Two Rocks':'WA'}], 
        'property_types':['House', 'ApartmentUnitFlat'],'bedrooms':3,'bathrooms':2, 'car_spaces':2,
        'date_posted': '2022-06-17', 'car_spaces':2, 'min_price':300, 'max_price':600,'loan_type':'Variable',
        'variable_loan_type':'Interest Only','lvr':80, 'loan_term':None, 'mortgage_interest':None}
    
class Test_Rates:
    def test_owner_occupier_fixed_rate_loan_term_5yr(self,monkeypatch):
        owner_occupier=property_notifier.Owner_Occupier()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','fixed',
        '80','5']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        owner_occupier.prompt()
        owner_occupier.fixed_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 3.84
    
    def test_owner_occupier_fixed_rate_loan_term_2yr(self,monkeypatch):
        owner_occupier=property_notifier.Owner_Occupier()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','fixed',
        '80','2']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        owner_occupier.prompt()
        owner_occupier.fixed_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 3.06
    
    def test_owner_occupier_variable_rate_principal_and_interest_lvr_80_loan_term_5yr(self,monkeypatch):
        owner_occupier=property_notifier.Owner_Occupier()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','Variable',
        'Principal and Interest','80','5']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        owner_occupier.prompt()
        owner_occupier.variable_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 2.46
    
    def test_owner_occupier_variable_rate_principal_and_interest_lvr_90_loan_term_5yr(self,monkeypatch):
        owner_occupier=property_notifier.Owner_Occupier()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','Variable',
        'Principal and Interest','90','5']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        owner_occupier.prompt()
        owner_occupier.variable_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 2.81
    
    def test_owner_occupier_variable_rate_interest_only_lvr_80_loan_term_5yr(self,monkeypatch):
        owner_occupier=property_notifier.Owner_Occupier()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','Variable',
        'Interest Only','80','5']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        owner_occupier.prompt()
        owner_occupier.variable_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 3.19
    
    def test_owner_occupier_variable_rate_interest_only_lvr_90_loan_term_5yr(self,monkeypatch):
        owner_occupier=property_notifier.Owner_Occupier()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','Variable',
        'Interest Only','90','5']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        owner_occupier.prompt()
        owner_occupier.variable_loan_rate(property_notifier.owner_occupier_rate_information)
        assert owner_occupier.__dict__['mortgage_interest'] == 3.50

    def test_investor_fixed_rate_loan_term_5yr(self,monkeypatch):
        investor=property_notifier.Investor()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','fixed',
        '80','5']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        investor.prompt()
        investor.fixed_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 4.11
    
    def test_investor_fixed_rate_loan_term_2yr(self,monkeypatch):
        investor=property_notifier.Investor()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','fixed',
        '80','2']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        investor.prompt()
        investor.fixed_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 3.34
    
    def test_investor_variable_rate_principal_and_interest_lvr_80_loan_term_5yr(self,monkeypatch):
        investor=property_notifier.Investor()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','Variable',
        'Principal and Interest','80','5']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        investor.prompt()
        investor.variable_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 2.80
    
    def test_investor_variable_rate_principal_and_interest_lvr_90_loan_term_5yr(self,monkeypatch):
        investor=property_notifier.Investor()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','Variable',
        'Principal and Interest','90','5']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        investor.prompt()
        investor.variable_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 3.11
    
    def test_investor_variable_rate_interest_only_lvr_80_loan_term_5yr(self,monkeypatch):
        investor=property_notifier.Investor()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','Variable',
        'Interest Only','80','5']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        investor.prompt()
        investor.variable_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 3.02
    
    def test_investor_variable_rate_interest_only_lvr_90_loan_term_5yr(self,monkeypatch):
        investor=property_notifier.Investor()
        inputs=['3','Madeley,Darch,Two Rocks','WA WA WA','House,Apartment','3','2','2','2022-06-17','300','600','Variable',
        'Interest Only','90','5']
        monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
        investor.prompt()
        investor.variable_loan_rate(property_notifier.investor_rate_information)
        assert investor.__dict__['mortgage_interest'] == 3.35

class Test_Access_Token:
    def test_connection(self):
        api=property_notifier.API()
        with requests_mock.mock() as m:
            m.post('https://auth.domain.com.au/v1/connect/token',json={'access_token':'token','expires_in':43200,'token_type':'Bearer'})
            response=requests.post('https://auth.domain.com.au/v1/connect/token',data={'client_id':api.client_id,
            'client_secret':api.client_secret,'grant_type':'client_credentials','scope':api.scopes, 'Content-Type':'text/json'})
            assert response.json()['access_token'] == 'token'

@pytest.fixture
def renter(monkeypatch):
    renter=property_notifier.Renter()
    inputs=['2','Hurstville, Penshurst','NSW NSW','House,Apartment','3','2','2','2022-06-17','500','800']
    monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
    renter.prompt()
    return renter

@pytest.fixture
def owner_occupier(monkeypatch):
    owner_occupier=property_notifier.Owner_Occupier()
    inputs=['2','Hurstville, Penshurst','NSW NSW','House,Apartment','3','2','2','2022-06-17','500','800',
    'Variable','Principal and Interest','80','5']
    monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
    owner_occupier.prompt()
    owner_occupier.variable_loan_rate(property_notifier.owner_occupier_rate_information)
    return owner_occupier

@pytest.fixture
def investor(monkeypatch):
    investor=property_notifier.Investor()
    inputs=['2','Hurstville, Penshurst','NSW NSW','House,Apartment','3','2','2','2022-06-17','500','800','Variable',
    'Principal and Interest','80','5']
    monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
    investor.prompt()
    investor.variable_loan_rate(property_notifier.investor_rate_information)
    return investor

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
def investor_interest_only(monkeypatch):
    investor=property_notifier.Investor()
    inputs=['2','Hurstville, Penshurst','NSW NSW','House,Apartment','3','2','2','2022-06-17','500','800','Variable',
    'Interest Only','80','5']
    monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
    investor.prompt()
    investor.variable_loan_rate(property_notifier.investor_rate_information)
    return investor

@pytest.fixture
def investor_fixed_rate(monkeypatch):
    investor=property_notifier.Investor()
    inputs=['2','Hurstville, Penshurst','NSW NSW','House,Apartment','3','2','2','2022-06-17','500','800','fixed',
    '80','5']
    monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
    investor.prompt()
    investor.fixed_loan_rate(property_notifier.investor_rate_information)
    return investor

@pytest.fixture
def owner_occupier_interest_only(monkeypatch):
    owner_occupier=property_notifier.Owner_Occupier()
    inputs=['2','Hurstville, Penshurst','NSW NSW','House,Apartment','3','2','2','2022-06-17','500','800',
    'Variable','Interest Only','80','5']
    monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
    owner_occupier.prompt()
    owner_occupier.variable_loan_rate(property_notifier.owner_occupier_rate_information)
    return owner_occupier

@pytest.fixture
def owner_occupier_fixed_rate(monkeypatch):
    owner_occupier=property_notifier.Owner_Occupier()
    inputs=['2','Hurstville, Penshurst','NSW NSW','House,Apartment','3','2','2','2022-06-17','500','800','fixed',
    '80','5']
    monkeypatch.setattr('builtins.input',lambda _: inputs.pop(0))
    owner_occupier.prompt()
    owner_occupier.fixed_loan_rate(property_notifier.owner_occupier_rate_information)
    return owner_occupier

class Test_Property_Calculations_Investor:
    def test_investor_calculation_house_data_interest_only(self,investor_interest_only,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.investor_calculation_house_data(investor_interest_only,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.44, 
        'Rental Income' : 800, 'Operating Expenses': 400.00, 'Cash Flow': 398.56, 'Cash on Cash Return': 33.45, '1yr Appreciation': 
        10, '5yr Appreciation': 50, '10yr Appreciation': 80}
    
    def test_investor_calculation_house_data_principal_and_interest(self,investor,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.investor_calculation_house_data(investor,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 10.23, 
        'Rental Income' : 800, 'Operating Expenses': 400.00, 'Cash Flow': 389.77, 'Cash on Cash Return': 32.71, '1yr Appreciation': 
        10, '5yr Appreciation': 50, '10yr Appreciation': 80}
    
    def test_investor_calculation_house_data_fixed_rate(self,investor_fixed_rate,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.investor_calculation_house_data(investor_fixed_rate,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 10.56, 
        'Rental Income' : 800, 'Operating Expenses': 400.00, 'Cash Flow': 389.44, 'Cash on Cash Return': 32.68, '1yr Appreciation': 
        10, '5yr Appreciation': 50, '10yr Appreciation': 80}
    
    def test_investor_calculation_apartment_data_interest_only(self,investor_interest_only,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.investor_calculation_apartment_data(investor_interest_only,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.44, 
        'Rental Income' : 750, 'Operating Expenses': 375.00, 'Cash Flow': 373.56, 'Cash on Cash Return': 31.35, '1yr Appreciation': 
        5, '5yr Appreciation': 10, '10yr Appreciation': 60}
    
    def test_investor_calculation_house_apartment_principal_and_interest(self,investor,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.investor_calculation_apartment_data(investor,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 10.23, 
        'Rental Income' : 750, 'Operating Expenses': 375.00, 'Cash Flow': 364.77, 'Cash on Cash Return': 30.61, '1yr Appreciation': 
        5, '5yr Appreciation': 10, '10yr Appreciation': 60}
    
    def test_investor_calculation_house_apartment_fixed_rate(self,investor_fixed_rate,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.investor_calculation_apartment_data(investor_fixed_rate,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 10.56, 
        'Rental Income' : 750, 'Operating Expenses': 375.00, 'Cash Flow': 364.44, 'Cash on Cash Return': 30.58, '1yr Appreciation': 
        5, '5yr Appreciation': 10, '10yr Appreciation': 60}
    
class Test_Property_Calculations_Owner_Occupier:
    def test_owner_occupier_calculation_house_data_interest_only(self,owner_occupier_interest_only,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.owner_occupier_calculation_house_data(owner_occupier_interest_only,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.52,  
        '10yr Appreciation': 80}

    def test_owner_occupier_calculation_house_data_principal_and_interest(self,owner_occupier,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.owner_occupier_calculation_house_data(owner_occupier,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 10.14, 
        '10yr Appreciation': 80}
    
    def test_owner_occupier_calculation_house_data_fixed_rate(self,owner_occupier_fixed_rate,property_data_withinput_house,suburb_performance_statistics_api_calls_house):
        property_notifier.owner_occupier_calculation_house_data(owner_occupier_fixed_rate,0,property_data_withinput_house,suburb_performance_statistics_api_calls_house)
        assert property_data_withinput_house[0]=={'Listing Date': '2022-07-05','Property Type': 'House', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 10.49, 
        '10yr Appreciation': 80}

    def test_owner_occupier_calculation_apartment_data_interest_only(self,owner_occupier_interest_only,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.owner_occupier_calculation_apartment_data(owner_occupier_interest_only,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 1.52, 
        '10yr Appreciation': 60}

    def test_owner_occupier_calculation_apartment_data_principal_and_interest(self,owner_occupier,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.owner_occupier_calculation_apartment_data(owner_occupier,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 10.14, 
        '10yr Appreciation': 60}
    
    def test_owner_occupier_calculation_apartment_data_fixed_rate(self,owner_occupier_fixed_rate,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment):
        property_notifier.owner_occupier_calculation_apartment_data(owner_occupier_fixed_rate,0,property_data_withinput_apartment,suburb_performance_statistics_api_calls_apartment)
        assert property_data_withinput_apartment[0]=={'Listing Date': '2022-07-05','Property Type': 'Apartment', 'Suburb': 'Hurstville','State': 'NSW',
        'Postcode': '2220', 'Address': '94 Queens Road, Hurstville', 'Land Area': 'N/A', 'Price': 715.00,
        'Url': 'https://www.domain.com.au/94-queens-road-hurstville-nsw-2220-15970998', 'Mortgage Repayments': 10.49, 
        '10yr Appreciation': 60}





