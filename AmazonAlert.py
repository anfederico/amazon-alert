# ----- Plotting Configuration -------------------------------------------------

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import DateFormatter
import numpy as np
import datetime as dt

def plotDatePrice(productID, productTitle, data):
    
    # Data setup 
    x, y = [], []
    for datapoint in data:
        date = datapoint.split('|')[0]
        price = float(datapoint.split('|')[1])
        x.append(dt.datetime.strptime(date, '%Y-%m-%d'))
        y.append(price)     
    x = matplotlib.dates.date2num(x)    
    x_np, y_np = np.array(x), np.array(y)   
    
    # Plot setup
    ax = plt.figure(figsize=(6, 3)).add_subplot(111)
    ax.spines['top'].set_visible(False)   
    ax.spines['right'].set_visible(False)   
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()   
    ax.plot(x_np, y_np, color='lightblue', lw=2)
    ax.margins(0.05)  
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: ('$%i' % (x))))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    plt.yticks(fontsize=8)
    plt.ylim(ymin=min(y)*0.7, ymax=max(y)*1.3)
    plt.title('Recent Price History\n'+productTitle, weight ='light', fontsize=12, y=1.08)  
    plt.xticks(rotation=40, fontsize=7) 
    plt.tight_layout()
    plt.savefig(productID+'.png')
    return productID+'.png'

# ----- Email Configuration ----------------------------------------------------

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def sendEmail(product, graph, EMAIL_CREDENTIALS):
    
    # Gmail credentials
    self = EMAIL_CREDENTIALS[0]
    password = EMAIL_CREDENTIALS[1]    
    fromAddr = EMAIL_CREDENTIALS[2]
    toAddr = EMAIL_CREDENTIALS[3]
    
    # Handle base
    msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddr
    msg['Subject'] = "Price Alert: " + product
    msgText = MIMEText('<center><br><img src="cid:image"><br></center>', 'html')
    msg.attach(msgText)
 
    # Embed image
    image = open(graph, 'rb')
    msgImage = MIMEImage(image.read())
    msgImage.add_header('Content-ID', '<image>')
    msg.attach(msgImage)
    image.close()     

    # Send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(self, password)
    text = msg.as_string()
    server.sendmail(fromAddr, toAddr, text)
    server.quit()
    
# ----- Amazon API -------------------------------------------------------------
    
from amazon.api import AmazonAPI    
import csv
import time

def readPrices(csvFile):
    priceData = {}
    targetData = {}
    with open(csvFile, 'rb') as infile:
        for line in infile:
            row = line.strip('\n\r').split(',')
            column = row[0].split('|')
            priceData[column[0]] = row[1:]
            targetData[column[0]] = column[1]
    infile.close()        
    return priceData, targetData
    
def updatePrices(newPriceData, oldPriceData):
    for pair in newPriceData:
        product = pair[0]
        price = pair[1]
        try: oldPriceData[product].append(price)
        except KeyError:
            print "Product %s was skipped." % (product)
            print "It has not been initalized with an alert price!"
    return oldPriceData
    
def writePrices(newPriceData, targetData, csvFile):
    with open(csvFile, 'wb') as outfile:
        writer = csv.writer(outfile)
        for product in newPriceData:
            target = targetData[product]
            writer.writerow([product+'|'+target]+newPriceData[product])
        outfile.close()         

def getPrice(productID, AWS_CREDENTIALS):
    amazon = AmazonAPI(AWS_CREDENTIALS[0], AWS_CREDENTIALS[1], AWS_CREDENTIALS[2])
    result = amazon.lookup(ItemId=productID)
    return result.title, result.price_and_currency[0]

def addProduct(productID, csvFile, alertWhen, alertType, AWS_CREDENTIALS):
    currentPrice = getPrice(productID, AWS_CREDENTIALS)[1]
    
    if alertType == "percentChange":
        delta = (float(alertWhen)/100)+1
        alertPrice = currentPrice*delta
    
    elif alertType == "desiredPrice":
        alertPrice = float(alertWhen)

    else: raise ValueError('Invalid alertType')
    
    with open(csvFile, 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([productID+'|'+str(alertPrice)]) 
        outfile.close()

def dailyScan(productIDs, csvFile, AWS_CREDENTIALS, EMAIL_CREDENTIALS):
    prices, targets = readPrices(csvFile)
    alerts = []
    update = []
    for productID in productIDs:
        title, price = getPrice(productID, AWS_CREDENTIALS)
        date = time.strftime("%Y-%m-%d") 
        update.append((productID,date+'|'+str(price)))
        
        try: 
            if price <= float(targets[productID]):
                alerts.append(productID)
        except KeyError: pass
    
    updatedPrices = updatePrices(update, prices)
    writePrices(updatedPrices, targets, csvFile)
    
    for alert in alerts:
        graph = plotDatePrice(alert, title, updatedPrices[alert])
        sendEmail(title, graph, EMAIL_CREDENTIALS)
