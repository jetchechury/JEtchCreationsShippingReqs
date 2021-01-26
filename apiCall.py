from bs4 import BeautifulSoup
import datetime
from selenium import webdriver


import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(options=chrome_options)


# def init_browser():
#     executable_path={'executable_path':'/usr/local/bin/chromedriver'}
#     return Browser('chrome', **executable_path, headless=True)


userID=config.userID
acceptTime="1600"
originZip="75244"

def verifyZip(destinationZip):
    urlZip=f"https://secure.shippingapis.com/ShippingAPI.dll?API=CityStateLookup&XML=<CityStateLookupRequest USERID={userID}><ZipCode ID='0'><Zip5>{destinationZip}</Zip5></ZipCode></CityStateLookupRequest>"
    browser.get(urlZip)
    html=browser.page_source
    # html=browser.html

    soup = BeautifulSoup(html, 'xml')
    if not soup.find('State'):
        zipStatus="incorrect"
    else:
        zipStatus="correct"

    return zipStatus


def firstClass(destinationZip,shipDate):
    mailClassFirst="3"
    urlFirstClass = f"https://secure.shippingapis.com/ShippingAPI.dll?API=SDCGetLocations&XML=<SDCGetLocationsRequest USERID={userID}><MailClass>{mailClassFirst}</MailClass><OriginZIP>{originZip}</OriginZIP><DestinationZIP>{destinationZip}</DestinationZIP><AcceptDate>{shipDate}</AcceptDate><AcceptTime>{acceptTime}</AcceptTime></SDCGetLocationsRequest>"
    #API Call for First Class Mail
    browser.get(urlFirstClass)
    html=browser.page_source
    # html=browser.html

    soup = BeautifulSoup(html, 'xml')
    destCity=soup.find('DestCity').text
    destState=soup.find('DestState').text
    destZip=soup.find('DestZIP').text
    shipDate=soup.find('AcceptDate').text

    schedDlvryDateFirstClass=soup.find('SchedDlvryDate').text


    return destCity,destState,destZip,shipDate,schedDlvryDateFirstClass


def priorityMail(destinationZip,shipDate):

    mailClassPriority="2"
    urlPriority = f"https://secure.shippingapis.com/ShippingAPI.dll?API=SDCGetLocations&XML=<SDCGetLocationsRequest USERID={userID}><MailClass>{mailClassPriority}</MailClass><OriginZIP>{originZip}</OriginZIP><DestinationZIP>{destinationZip}</DestinationZIP><AcceptDate>{shipDate}</AcceptDate><AcceptTime>{acceptTime}</AcceptTime></SDCGetLocationsRequest>"
    #API Call for Priority Mail
    browser.get(urlPriority)
    html=browser.page_source

    soup = BeautifulSoup(html, 'xml')
    schedDlvryDatePriority=soup.find('SDD').text
    # driver.quit()
    # browser.quit()

    return schedDlvryDatePriority


def priorityMailExpress(destinationZip,shipDate):

    mailClassPriorityExp="1"
    urlPriorityExpress = f"https://secure.shippingapis.com/ShippingAPI.dll?API=SDCGetLocations&XML=<SDCGetLocationsRequest USERID={userID}><MailClass>{mailClassPriorityExp}</MailClass><OriginZIP>{originZip}</OriginZIP><DestinationZIP>{destinationZip}</DestinationZIP><AcceptDate>{shipDate}</AcceptDate><AcceptTime>{acceptTime}</AcceptTime></SDCGetLocationsRequest>"
    #API Call for Priority Expresss Mail
    # driver.get(urlPriorityExpress)
    browser.get(urlPriorityExpress)
    html=browser.page_source

    soup = BeautifulSoup(html, 'xml')
    schedDlvryDatePriorityExpress=soup.find('SDD').text
    # driver.quit()
    # browser.quit()

    return schedDlvryDatePriorityExpress



def date_by_adding_business_days(from_date, add_days):
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        holidays =[datetime.datetime(2020,1,1),datetime.datetime(2020,1,20),datetime.datetime(2020,2,17),datetime.datetime(2020,5,25),datetime.datetime(2020,7,3),datetime.datetime(2020,7,4),datetime.datetime(2020,9,7),datetime.datetime(2020,10,12),datetime.datetime(2020,11,11),datetime.datetime(2020,11,26),datetime.datetime(2020,11,27),datetime.datetime(2020,12,24),datetime.datetime(2020,12,25),datetime.datetime(2020,12,31)]
        if weekday >= 5: # sunday = 6
            continue
        if current_date in holidays:
            continue
        business_days_to_add -= 1
    return current_date

def date_by_subtracting_business_days(eventDate, minus_days):
    business_days_to_subtract = minus_days
    current_date = eventDate
    while business_days_to_subtract > 0:
        #subtract one day from event date
        current_date -= datetime.timedelta(days=1)
        #determine day of week and assign it an integer value
        weekday = current_date.weekday()
        holidays =[datetime.datetime(2020,1,1),datetime.datetime(2020,1,20),datetime.datetime(2020,2,17),datetime.datetime(2020,5,25),datetime.datetime(2020,7,3),datetime.datetime(2020,7,4),datetime.datetime(2020,9,7),datetime.datetime(2020,10,12),datetime.datetime(2020,11,11),datetime.datetime(2020,11,26),datetime.datetime(2020,11,27),datetime.datetime(2020,12,24),datetime.datetime(2020,12,25),datetime.datetime(2020,12,31)]
        if weekday >= 5: # saturday=5 sunday = 6
            continue
        if current_date in holidays:
            continue
        business_days_to_subtract -= 1
    return current_date

def outputdateformatter(item):
        datetimeObject=datetime.datetime.strptime(item, '%Y-%m-%d')
        dateString=datetimeObject.strftime("%a, %b %d")
        return dateString