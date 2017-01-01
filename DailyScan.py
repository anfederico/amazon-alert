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

def main():
    csvFile = 'priceHistory.csv'
    products = ['B01GW3H3U8', 'B01DFKC2SO', 'B00DB9JV5W']
    dailyScan(products, csvFile, AWS_CREDENTIALS, EMAIL_CREDENTIALS) 

if __name__ == '__main__':
    main()
  