import unittest
from cheapest_shopping import shopping_list,food

class test_list(unittest.TestCase):
    
    shopping=shopping_list()
    
    def add_with_default(self):
        oats=food('Uncle Tobys',1)
        
        

if __name__=='__main__':
    unittest.main()
