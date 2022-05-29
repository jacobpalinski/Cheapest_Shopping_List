from bs4 import BeautifulSoup

woolworths_base_url='https://www.woolworths.com.au/shop/search/products?searchTerm='
coles_base_url='https://shop.coles.com.au/a/a-national/everything/search/'

class shopping_list:

    def __init__(self):
        self.list=[]
    
    def new_item(self,food):
        self.list.append({'name':food.name,'quantity':food.quantity,'size':food.size,
        'brand':food.brand})

class food:

    def __init__(self,name,quantity,size=None,brand=None):
        self.name=name
        self.quantity=quantity
        self.size=size
        self.brand=brand

class product_information:

    def __init__(self):
        self.product_info=[]

    def get_data(self):
        pass

    def cheapest_items(self):
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




