<p align="center"><img src="https://raw.githubusercontent.com/anfederico/Amazon-Alert/master/AlertLogo.png" width=225px><p>

## External Libraries
```text
matplotlib
numpy
datetime
smtplib
amazonapi
```
## Required Accounts
```text
To do this you'll need two free accounts
1. Amazon Web Services
2. Google Mail
```
<i><a href='https://affiliate-program.amazon.com/gp/advertising/api/detail/main.html'> 
Sgn up for a product advertising account after you create your AWS credentials</a></i>

## Code Examples

#### Run Once for Initial Setup

```python
from AmazonAlert import addProduct, dailyScan

# ----- Gmail Credentials -----------

# This gives your script access to your gmail account, may want to use a throwaway
# Make sure "Allow Access To Less Secure Apps" is turned on in gmail settings
EMAIL_SELF = 'youremail@gmail.com'
EMAIL_PASSWORD = 'yourpassword'    

# If using a throwaway, adjust EMAIL_TO to your real email!
EMAIL_FROM = EMAIL_SELF     
EMAIL_TO = EMAIL_SELF
EMAIL_CREDENTIALS = [EMAIL_SELF, EMAIL_PASSWORD, EMAIL_FROM, EMAIL_TO]
 
# ----- Amazon Credentials -----------

AWS_ACCESS_KEY_ID = 'Your AWS Access Key ID'
AWS_SECRET_ACCESS_KEY = 'Your AWS Secret Access Key'
AWS_ASSOCIATE_TAG = 'Your AWS Associate Tag'
AWS_CREDENTIALS = [AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG]        

# This file will hold all of our data
csvFile = 'priceHistory.csv'

# Before you start monitoring a product, add it to the data file
# For each product you add, you're also giving directions for a target price

# Xbox Wireless Controller
# Alert when current price drops at least 50%
addProduct('B01GW3H3U8', csvFile, -50, 'percentChange', AWS_CREDENTIALS)  

# Echo Dot
# Alert when current price drops at least 25%
addProduct('B01DFKC2SO', csvFile, -25, 'percentChange', AWS_CREDENTIALS) 

# Halo 5
# Alert when current price drops to at least $19.99
addProduct('B00DB9JV5W', csvFile, 19.99, 'desiredPrice', AWS_CREDENTIALS)

# You can also append new products at a later time to the same data file
```

#### priceHistory.csv
```text
B01GW3H3U8|24.755
B01DFKC2SO|37.4925
B00DB9JV5W|19.99
```

#### Daily Monitoring of Prices
```python
from AmazonAlert import addProduct, dailyScan

# ----- Gmail Credentials -----------

EMAIL_SELF = 'youremail@gmail.com'
EMAIL_PASSWORD = 'yourpassword'    
EMAIL_FROM = EMAIL_SELF     
EMAIL_TO = EMAIL_SELF
EMAIL_CREDENTIALS = [EMAIL_SELF, EMAIL_PASSWORD, EMAIL_FROM, EMAIL_TO]
 
# ----- Amazon Credentials -----------

AWS_ACCESS_KEY_ID = 'Your AWS Access Key ID'
AWS_SECRET_ACCESS_KEY = 'Your AWS Secret Access Key'
AWS_ASSOCIATE_TAG = 'Your AWS Associate Tag'
AWS_CREDENTIALS = [AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_ASSOCIATE_TAG]        

# You should run this file on a dedicated server once or multiple times a day
# Personally, I run it daily at pythonanywhere.com
# Make sure all products have been properly initalized in the csvFile
# Otherwise they'll be skipped
# If any products fall below their target, you'll receieve an email!

def main():
    csvFile = 'priceHistory.csv'
    products = ['B01GW3H3U8', 'B01DFKC2SO', 'B00DB9JV5W']
    dailyScan(products, csvFile, AWS_CREDENTIALS, EMAIL_CREDENTIALS) 

if __name__ == '__main__':
    main()
```

#### Updated priceHistory.csv
```text
B01GW3H3U8|24.755,2016-12-15|49.0
B01DFKC2SO|37.4925,2016-12-15|49.99
B00DB9JV5W|19.99,2016-12-15|24.78
```

#### Email Layout
<img src="https://raw.githubusercontent.com/anfederico/Amazon-Alert/master/AlertEmail.png" width=100%>
