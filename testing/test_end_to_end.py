import pytest
import pytest_mock
import time
import datetime
from application import application
from flask import request
from property_notifier import *
from decimal import Decimal
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv

# Activate flask application from command prompt before running tests

load_dotenv()

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.close()
    driver.quit()

@pytest.fixture(params = [('kpalinski99@gmail.com', os.environ.get('GOOGLE_IN_APP_PASSWORD')), ('jacob.palinski@outlook.com', os.environ.get('MICROSOFT_OUTLOOK_PASSWORD'))])
def driver_initial_page_renter(driver, request):
    driver.get('http://127.0.0.1:5000/initial_page')
    user_type = Select(driver.find_element(By.XPATH, '//*[@id="user_type"]'))
    user_type.select_by_value('Renter')
    email = driver.find_element(By.XPATH, '//*[@id="email"]')
    email.clear()
    email.send_keys(request.param[0])
    password = driver.find_element(By.XPATH, '//*[@id="password"]')
    password.clear()
    password.send_keys(request.param[1])
    driver.find_element(By.XPATH, '//*[@id="next"]').click()
    return driver
    
@pytest.fixture
def driver_renter_page_no_flash_message(driver_initial_page_renter):
    driver = driver_initial_page_renter
    locations = driver.find_element(By.XPATH, '//*[@id="locations"]')
    locations.clear()
    locations.send_keys('(Hurstville,NSW,2220),(Penshurst,NSW,2222)')
    property_types = Select(driver.find_element(By.XPATH, '//*[@id="property_types"]'))
    property_types.select_by_value('House')
    property_types.select_by_value('Townhouse')
    bedrooms = Select(driver.find_element(By.XPATH, '//*[@id="bedrooms"]'))
    bedrooms.select_by_value('2')
    bathrooms = Select(driver.find_element(By.XPATH, '//*[@id="bathrooms"]'))
    bathrooms.select_by_value('2')
    car_spaces = Select(driver.find_element(By.XPATH, '//*[@id="car_spaces"]'))
    car_spaces.select_by_value('2')
    earliest_posting_date = driver.find_element(By.XPATH, '//*[@id="date_posted"]')
    earliest_posting_date.clear()
    earliest_posting_date.send_keys('01032023')
    max_price = driver.find_element(By.XPATH, '//*[@id="max_price"]')
    max_price.clear()
    max_price.send_keys(800)
    min_price = driver.find_element(By.XPATH, '//*[@id="min_price"]')
    min_price.clear()
    min_price.send_keys(600)
    driver.find_element(By.XPATH, '//*[@id="next"]').click()
    return driver

@pytest.fixture
def driver_renter_page_flash_message(driver_initial_page_renter):
    driver = driver_initial_page_renter
    locations = driver.find_element(By.XPATH, '//*[@id="suburbs"]')
    locations.clear()
    locations.send_keys('(Hurstville,NSW,2220),(Penshurst,NSW,2222)')
    property_types = Select(driver.find_element(By.XPATH, '//*[@id="property_types"]'))
    property_types.select_by_value('House')
    property_types.select_by_value('Townhouse')
    bedrooms = Select(driver.find_element(By.XPATH, '//*[@id="bedrooms"]'))
    bedrooms.select_by_value('2')
    bathrooms = Select(driver.find_element(By.XPATH, '//*[@id="bathrooms"]'))
    bathrooms.select_by_value('2')
    car_spaces = Select(driver.find_element(By.XPATH, '//*[@id="car_spaces"]'))
    car_spaces.select_by_value('2')
    earliest_posting_date = driver.find_element(By.XPATH, '//*[@id="date_posted"]')
    earliest_posting_date.clear()
    earliest_posting_date.send_keys('01032023')
    max_price = driver.find_element(By.XPATH, '//*[@id="max_price"]')
    max_price.clear()
    max_price.send_keys(200)
    min_price = driver.find_element(By.XPATH, '//*[@id="min_price"]')
    min_price.clear()
    min_price.send_keys(100)
    driver.find_element(By.XPATH, '//*[@id="next"]').click()
    return driver

class Test_End_To_End_Renter:
    def test_renter_end_to_end_no_flash_message(self,driver, driver_initial_page_renter, driver_renter_page_no_flash_message):
        driver = driver_renter_page_no_flash_message
        assert 'Thank You' in driver.title

    def test_renter_end_to_end_flash_message(self,driver, driver_initial_page_renter, driver_renter_page_flash_message):
        driver = driver_renter_page_flash_message
        assert '<div class="alert no results">' in driver.page_source

@pytest.fixture(params=[('Investor', 'kpalinski99@gmail.com', os.environ.get('GOOGLE_IN_APP_PASSWORD')), ('Investor', 'jacob.palinski@outlook.com', os.environ.get('MICROSOFT_OUTLOOK_PASSWORD')),
('Owner Occupier', 'kpalinski99@gmail.com', os.environ.get('GOOGLE_IN_APP_PASSWORD')), ('Owner Occupier', 'jacob.palinski@outlook.com', os.environ.get('MICROSOFT_OUTLOOK_PASSWORD'))])
def driver_initial_page_investor_and_owner_occupier(driver, request):
    driver.get('http://127.0.0.1:5000/initial_page')
    user_type = Select(driver.find_element(By.XPATH, '//*[@id="user_type"]'))
    user_type.select_by_value(request.param[0])
    email = driver.find_element(By.XPATH, '//*[@id="email"]')
    email.clear()
    email.send_keys(request.param[1])
    password = driver.find_element(By.XPATH, '//*[@id="password"]')
    password.clear()
    password.send_keys(request.param[2])
    driver.find_element(By.XPATH, '//*[@id="next"]').click()
    return driver

@pytest.fixture
def driver_investor_and_owner_occupier_page_no_flash_message(driver_initial_page_investor_and_owner_occupier):
    driver = driver_initial_page_investor_and_owner_occupier
    locations = driver.find_element(By.XPATH, '//*[@id="suburbs"]')
    locations.clear()
    locations.send_keys('(Hurstville,NSW,2220),(Penshurst,NSW,2222)')
    property_types = Select(driver.find_element(By.XPATH, '//*[@id="property_types"]'))
    property_types.select_by_value('House')
    property_types.select_by_value('Townhouse')
    bedrooms = Select(driver.find_element(By.XPATH, '//*[@id="bedrooms"]'))
    bedrooms.select_by_value('2')
    bathrooms = Select(driver.find_element(By.XPATH, '//*[@id="bathrooms"]'))
    bathrooms.select_by_value('2')
    car_spaces = Select(driver.find_element(By.XPATH, '//*[@id="car_spaces"]'))
    car_spaces.select_by_value('2')
    earliest_posting_date=driver.find_element(By.XPATH, '//*[@id="date_posted"]')
    earliest_posting_date.clear()
    earliest_posting_date.send_keys('01032023')
    max_price=driver.find_element(By.XPATH, '//*[@id="max_price"]')
    max_price.clear()
    max_price.send_keys(1500000)
    min_price = driver.find_element(By.XPATH, '//*[@id="min_price"]')
    min_price.clear()
    min_price.send_keys(1000000)
    loan_type = Select(driver.find_element(By.XPATH, '//*[@id="loan_type"]'))
    loan_type.select_by_value('Fixed')
    variable_loan_type = Select(driver.find_element(By.XPATH, '//*[@id="variable_loan_type"]'))
    variable_loan_type.select_by_value('None')
    lvr=driver.find_element(By.XPATH, '//*[@id="lvr"]')
    lvr.clear()
    lvr.send_keys(80)
    loan_term=driver.find_element(By.XPATH, '//*[@id="loan_term"]')
    loan_term.clear()
    loan_term.send_keys(3)
    driver.find_element(By.XPATH, '//*[@id="next"]').click()
    return driver

@pytest.fixture
def driver_investor_and_owner_occupier_page_flash_message(driver_initial_page_investor_and_owner_occupier):
    driver = driver_initial_page_investor_and_owner_occupier
    locations = driver.find_element(By.XPATH,'//*[@id="suburbs"]')
    locations.clear()
    locations.send_keys('(Hurstville,NSW,2220),(Penshurst,NSW,2222)')
    property_types = Select(driver.find_element(By.XPATH, '//*[@id="property_types"]'))
    property_types.select_by_value('House')
    property_types.select_by_value('Townhouse')
    bedrooms = Select(driver.find_element(By.XPATH, '//*[@id="bedrooms"]'))
    bedrooms.select_by_value('2')
    bathrooms = Select(driver.find_element(By.XPATH, '//*[@id="bathrooms"]'))
    bathrooms.select_by_value('2')
    car_spaces = Select(driver.find_element(By.XPATH, '//*[@id="car_spaces"]'))
    car_spaces.select_by_value('2')
    earliest_posting_date = driver.find_element(By.XPATH, '//*[@id="date_posted"]')
    earliest_posting_date.clear()
    earliest_posting_date.send_keys('01032023')
    max_price = driver.find_element(By.XPATH, '//*[@id="max_price"]')
    max_price.clear()
    max_price.send_keys(200)
    min_price = driver.find_element(By.XPATH, '//*[@id="min_price"]')
    min_price.clear()
    min_price.send_keys(100)
    loan_type = Select(driver.find_element(By.XPATH, '//*[@id="loan_type"]'))
    loan_type.select_by_value('Fixed')
    variable_loan_type = Select(driver.find_element(By.XPATH, '//*[@id="variable_loan_type"]'))
    variable_loan_type.select_by_value('None')
    lvr = driver.find_element(By.XPATH,'//*[@id="lvr"]')
    lvr.clear()
    lvr.send_keys(80)
    loan_term = driver.find_element(By.XPATH, '//*[@id="loan_term"]')
    loan_term.clear()
    loan_term.send_keys(3)
    driver.find_element(By.XPATH, '//*[@id="next"]').click()
    return driver

class Test_End_To_End_Investor_and_Owner_Occupier:
    def test_investor_and_owner_occupier_end_to_end_no_flash_message(self, driver, driver_initial_page_investor_and_owner_occupier, driver_investor_and_owner_occupier_page_no_flash_message):
        driver = driver_investor_and_owner_occupier_page_no_flash_message
        assert 'Thank You' in driver.title

    def test_investor_and_owner_occupier_end_to_end_flash_message(self,driver, driver_initial_page_investor_and_owner_occupier, driver_investor_and_owner_occupier_page_flash_message):
        driver = driver_investor_and_owner_occupier_page_flash_message
        assert '<div class="alert no results">' in driver.page_source



