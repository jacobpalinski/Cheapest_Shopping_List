class User:
    def __init__(self):
        self.user_type=None
        self.suburb=[]
        self.property_type=[]
        self.min_price=None
        self.max_price=None
        self.area=None
        self.date_posted=None #Earliest Date Posting when searching for property
        self.car_spaces=None
        self.desired_demographic=None
        self.target_appreciation=None
        self.target_rentalyield=None
    
    def prompt(self):
        pass

class API:
    def __init__(self):
        self.client_id=None
        self.accesskey=None
    
    def authenticate(self):
        pass

class Property_Data:
    def __init__(self):
        self.property_list=[]
    
    def listings_search(self):
        pass

    def listings_info(self):
        pass

    def demographics(self):
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




