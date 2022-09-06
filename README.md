# Property_Notifier
### Project Purpose
Domain.com.au is one of Australia's major real estate portals. One flaw of the website is that it doesn't offer customised property information and on available listings for specific user purposes, whether it be renting, buying their first home or looking at properties for investment. Additionally users, have to look at all listings and search through multiple pages, to find listings most relevant to them and to make comparisons, which is an inefficient process. 

The Property_Notifier application aims to solve this issue by allowing users to provide customised information based on their needs, with the application then retrieving data from relevant Domain API's and performing calculations, with the end ouput being a customised CSV available for viewing via the users email. 

### How It Works
The user starts at http://flask-env.eba-jkgdj6x4.us-east-2.elasticbeanstalk.com/initial_page where they answer a question asking about their intended purpose for using the application and provide their email and relevant password (Note: Only Gmail and Microsoft accounts will be accepted). Upon clicking the Next button, the user will then be redirected to a webpage ending in /investor, /owner_occupier or /renter depending on the intended purpose selected on /initial_page. If the user form submitted on these pages meets validation criterea, and properties exist in the API's as per the information they have provided, an email containing a CSV with relevant property information and data will be sent, and the user will be redirected to the /thankyou page. 

#### Investor CSV Information and Data
* Listing Date
* Property Type
* Suburb
* State
* Postcode
* Address
* Land Area (if applicable)
* Price
* Url
* Mortgage Repayments (Monthly)
* Rental Income (Monthly)
* Operating Expenses (Monthly)
* Cash Flow (Monthly)
* Cash on Cash Return
* 1yr Appreciation
* 5yr Appreciation
* 10yr Appreciation

#### Owner Occupier CSV Information and Data
* Listing Date
* Property Type
* Suburb
* State
* Postcode
* Address
* Land Area (if applicable)
* Price
* Url
* Mortgage Repayments (Monthly)
* 10yr Appreciation (Monthly)

#### Renter CSV Information and Data
* Listing Date
* Property Type
* Suburb
* State
* Postcode
* Address
* Land Area (if applicable)
* Url
* Weekly Rent
* Annual Rent

### Tools/Technologies
Python, HTML, CSS, Flask, AWS Elastic Beanstalk

