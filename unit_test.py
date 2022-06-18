import unittest
from property_notifier import *


class test_list(unittest.TestCase):
    
    def test_correct_attributes_home_buyer(self):
        home_buyer=User()
        home_buyer.prompt()
        print(home_buyer.__dict__)
        self.assertEqual(home_buyer.__dict__,{'user_type': 'Home Buyer', 'suburbs': ['Madeley','Darch', 'Two Rocks'], 
        'property_types':['Houses', 'Apartments'],'min_price':400000, 'max_price':600000, 'bedrooms':3,
        'bathrooms':2, 'area': 300,'date_posted': '2022-06-17', 'car_spaces':2, 
        'desired_demographic': 'Under 20', 'target_appreciation': 5.1, 'target_rentalyield': 3.5})
    
    def test_correct_attributes_renter(self):
        renter=User()
        renter.prompt()
        print(renter.__dict__)
        self.assertEqual(renter.__dict__,{'user_type': 'Renter', 'suburbs': ['Madeley','Darch', 'Two Rocks'], 
        'property_types':['Houses', 'Apartments'],'min_price':400000, 'max_price':600000, 'bedrooms':3,
        'bathrooms':2, 'area': 300,'date_posted': '2022-06-17', 'car_spaces':2, 
        'desired_demographic': 'Under 20', 'target_appreciation': None, 'target_rentalyield': None})
    
    def test_access_token(self):
        domain_api=API()
        domain_api.authenticate()
        self.assertTrue(domain_api.access_token,domain_api.access_token!=None)


if __name__=='__main__':
    test_access=test_list()
    test_access.test_access_token()
