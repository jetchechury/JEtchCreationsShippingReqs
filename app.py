#!/usr/bin/python3.7

from flask import Flask, render_template, request
import datetime
from apiCall import date_by_adding_business_days
from apiCall import firstClass
from apiCall import outputdateformatter
from apiCall import priorityMail
from apiCall import priorityMailExpress
from apiCall import verifyZip
from apiCall import date_by_subtracting_business_days

#Create instance of Flask
app=Flask(__name__)

#Route to render index.html template using data from Mongo
@app.route("/")
def home():

    return render_template("index.html")

@app.route("/", methods=['POST','GET'])
def USPSAPI():
    # try:
    if request.method == 'POST':
        zipCode=request.form.get('zipCode')
        inputDate=request.form.get('orderDate')
        eventDate=request.form.get('eventDate')

        zipStatus=verifyZip(zipCode)
        try:
            if zipStatus== 'correct':
                # deliveryOpts={}
                #Change input dates to datetime objects
                orderDate=datetime.datetime.strptime(inputDate, '%m/%d/%Y')
                eventDate=datetime.datetime.strptime(eventDate, '%m/%d/%Y')

                #Calculate target delivery date
                targetDelivery=(date_by_subtracting_business_days(eventDate,2))

                #Calculate ready to ship date
                standardProcessingTime=(date_by_adding_business_days(orderDate,7))
                rushProcessingTime=(date_by_adding_business_days(orderDate,2))
                #Transform ready to ship dates to format compatiable with API
                shipDateStandard=standardProcessingTime.strftime("%d-%b-%Y")
                shipDateRush=rushProcessingTime.strftime("%d-%b-%Y")


                #Perform API call - FIRST CLASS STANDARD
                firstClassMailList=firstClass(zipCode,shipDateStandard)

                #Define universal variables
                destCity=f"{firstClassMailList[0]},"
                destState=firstClassMailList[1]
                destZIP=firstClassMailList[2]

                #Format Ship Date - Standard Processing
                shipDateStd=outputdateformatter(firstClassMailList[3])

                #Calculate First Class Mail Delivery Window - Standard Processing
                firstClassMinDateStd=datetime.datetime.strptime(firstClassMailList[4], '%Y-%m-%d')
                firstClassMaxDateStd=(date_by_adding_business_days(firstClassMinDateStd,2))

                #evaluate to generate row header
                if firstClassMaxDateStd > targetDelivery:
                    fcstdRowHeader="First Class Mail**"
                    fcstdRowHeader2="NOT RECOMMENDED"
                else:
                    daystillEvent=eventDate-firstClassMaxDateStd
                    daystillEventinDays=daystillEvent.days
                    fcstdRowHeader="First Class Mail**"
                    fcstdRowHeader2=f"Arrives {daystillEventinDays} day(s) before event date"

                #add to dictionary to evaluate for recommendations
                # deliveryOpts["Standard_Processing_/_Free_Shipping"]=firstClassMaxDateStd

                firstClassMinDateStd=firstClassMinDateStd.strftime("%a, %b %d")
                firstClassMaxDateStd=firstClassMaxDateStd.strftime("%a, %b %d")



                #Perform API call - FIRST CLASS RUSH
                firstClassMailListRush=firstClass(zipCode,shipDateRush)

                #Format Ship Date - Standard Processing
                shipDateRush=outputdateformatter(firstClassMailListRush[3])

                #Calculate First Class Mail Delivery Window - Rush Processing
                firstClassMinDateRush=datetime.datetime.strptime(firstClassMailListRush[4], '%Y-%m-%d')
                firstClassMaxDateRush=(date_by_adding_business_days(firstClassMinDateRush,2))

                #evaluate to generate row header
                if firstClassMaxDateRush > targetDelivery:
                    fcrushRowHeader="First Class Mail**"
                    fcrushRowHeader2="NOT RECOMMENDED"
                else:
                    daystillEvent=eventDate-firstClassMaxDateRush
                    daystillEventinDays=daystillEvent.days
                    fcrushRowHeader="First Class Mail**"
                    fcrushRowHeader2=f"Arrives {daystillEventinDays} day(s) before event date"

                #add to dictionary to evaluate for recommendations
                # deliveryOpts["Rush_Processing_/_Free_Shipping"]=firstClassMaxDateRush

                firstClassMinDateRush=firstClassMinDateRush.strftime("%a, %b %d")
                firstClassMaxDateRush=firstClassMaxDateRush.strftime("%a, %b %d")



                #Perform API call - PRIORITY STANDARD
                priorityMailListStd=priorityMail(zipCode,shipDateStandard)

                #PM to datetime object
                PMDT=datetime.datetime.strptime(priorityMailListStd, '%Y-%m-%d')

                #evaluate to generate row header
                if PMDT > targetDelivery:
                    pmstdRowHeader="Priority Mail"
                    pmstdRowHeader2="NOT RECOMMENDED"
                else:
                    daystillEvent=eventDate-PMDT
                    daystillEventinDays=daystillEvent.days
                    pmstdRowHeader="Priority Mail"
                    pmstdRowHeader2=f"Arrives {daystillEventinDays} day(s) before event date"

                #Format Priority Mail Output Date - Standard Processing
                priorityDateStd=outputdateformatter(priorityMailListStd)

               #Perform API call - PRIORITY RUSH
                priorityMailListRush=priorityMail(zipCode,shipDateRush)

                #PM to datetime object
                PMRDT=datetime.datetime.strptime(priorityMailListRush, '%Y-%m-%d')

                #evaluate to generate row header
                if PMRDT > targetDelivery:
                    pmrRowHeader="Priority Mail"
                    pmrRowHeader2="NOT RECOMMENDED"
                else:
                    daystillEvent=eventDate-PMRDT
                    daystillEventinDays=daystillEvent.days
                    pmrRowHeader="Priority Mail"
                    pmrRowHeader2=f"Arrives {daystillEventinDays} day(s) before event date"

                #Format Priority Mail Output Date - Standard Processing
                priorityDateRush=outputdateformatter(priorityMailListRush)

                #Perform API call - PRIORITY EXP STANDARD
                priorityExpMailListStd=priorityMailExpress(zipCode,shipDateStandard)

                #PM to datetime object
                PMEDT=datetime.datetime.strptime(priorityExpMailListStd, '%Y-%m-%d')

                #evaluate to generate row header
                if PMEDT > targetDelivery:
                    pmeRowHeader="Priority Mail Express*"
                    pmeRowHeader2="NOT RECOMMENDED"
                else:
                    daystillEvent=eventDate-PMEDT
                    daystillEventinDays=daystillEvent.days
                    pmeRowHeader="Priority Mail Express*"
                    pmeRowHeader2=f"Arrives {daystillEventinDays} day(s) before event date"

                #Format Priority Mail Output Date - Standard Processing
                priorityExpDateStd=outputdateformatter(priorityExpMailListStd)

                #Perform API call - PRIORITY EXP RUSH
                priorityExpMailListRush=priorityMailExpress(zipCode,shipDateRush)
                #add to dictionary to evaluate for recommendations
                PMERDT=datetime.datetime.strptime(priorityExpMailListRush, '%Y-%m-%d')

                #evaluate to generate row header
                if PMERDT > targetDelivery:
                    pmerRowHeader="Priority Mail Express*"
                    pmerRowHeader2="NOT RECOMMENDED"
                else:
                    daystillEvent=eventDate-PMERDT
                    daystillEventinDays=daystillEvent.days
                    pmerRowHeader="Priority Mail Express*"
                    pmerRowHeader2=f"Arrives {daystillEventinDays} day(s) before event date"

                #Format Priority Mail Output Date - Rush Processing
                priorityExpDateRush=outputdateformatter(priorityExpMailListRush)




                #Format Order Date to include day of week
                orderDateP=orderDate.strftime("%A, %B %d")
                eventDate=eventDate.strftime("%A, %B %d")

                #Generate recommendations list
                # recommendations=[]
                # for key,value in deliveryOpts:
                #     #if date is before target delivery date (2 days before event)
                #     if value <= targetDelivery:
                #         #replace characters to label recommendations
                #         label=key.replace("_", " ").replace("/","with").replace("*","Shipping")
                #         print(label)
                #         daystillEvent=eventDate-value
                #         recommendations.append(f"{label} will arrive {daystillEvent.days} days before your event")
                #     else:
                #         label=key.replace("_", " ").replace("/","with").replace("*","Shipping")
                #         print(label)
                #         recommendations.append(f"X {label}-NOT RECOMMENDED")

                # recommendation1=recommendations[0]
                # recommendation2=recommendations[1]
                # recommendation3=recommendations[2]
                # recommendation4=recommendations[3]
                # recommendation5=recommendations[4]
                # # recommendation6=recommendations[5]
# recommendation5=recommendation5,recommendation4=recommendation4,recommendation3=recommendation3,recommendation2=recommendation2,recommendation1=recommendation1

                # return render_template('transit.html',days=dayspmstdRowHeader, minProcessingOutput=minProcessingOutput, shippingMin=shippingMin)
                return render_template('index.html',pmerRowHeader=pmerRowHeader,pmerRowHeader2=pmerRowHeader2,pmeRowHeader=pmeRowHeader,pmeRowHeader2=pmeRowHeader2,pmrRowHeader=pmrRowHeader,pmrRowHeader2=pmrRowHeader2,pmstdRowHeader=pmstdRowHeader,pmstdRowHeader2=pmstdRowHeader2,fcrushRowHeader=fcrushRowHeader,fcrushRowHeader2=fcrushRowHeader2,fcstdRowHeader2=fcstdRowHeader2,fcstdRowHeader=fcstdRowHeader,eventDate=eventDate,priorityExpDateRush=priorityExpDateRush,priorityExpDateStd=priorityExpDateStd,inputDate=orderDateP,destCity=destCity,destState=destState,destZIP=destZIP,shipDateStd=shipDateStd,firstClassMinDateStd=firstClassMinDateStd,firstClassMaxDateStd=firstClassMaxDateStd,priorityDateStd=priorityDateStd,shipDateRush=shipDateRush,firstClassMinDateRush=firstClassMinDateRush,firstClassMaxDateRush=firstClassMaxDateRush,priorityDateRush=priorityDateRush)

            else:
                return render_template('error-zip.html',zipCode=zipCode)

        except AttributeError as e:
            if "'NoneType' object has no attribute 'text'" in str(e):
                return render_template('error-date.html')
        except ValueError as v:
            if "time data" in str(v):
                return render_template('error-date-format.html',inputDate=inputDate,eventDate=eventDate)
        # except:
            # return render_template('index.html')

    return render_template('index.html')
    # except AttributeError as e:
        # if "'NoneType' object has no attribute 'text'" in str(e):
            # return render_template('error-date.html')
        # else:
            # return render_template('error-zipCode.html')






if __name__=="__main__":
    app.run()