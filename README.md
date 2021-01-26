# JEtchCreationsShippingReqs

# USPS Service Commitment Webpage

## Objective

To create a webpage that would provide customers with accurate shipping information tailored to J. Etch Creation processing time.

## The Process

A Python script was created to make a web-based application that allows customers to enter their order information and return all available shipping options and recommendations . To accomplish this, [Flask](https://flask.palletsprojects.com/en/1.1.x/) and the [USPS API](https://www.usps.com/business/web-tools-apis/documentation-updates.htm) were used.

The application takes into account the customer's order date, event date, and zip code.  Once this information has been entered information for all shipping methods offered by J. Etch Creations is gathered through a series of USPS API calls.  A table is then populated with the information gathered.  In addition to shipping and delivery dates that table provides the customer with recommendations based on their needs.


## Future Advancements

In the future I hope to improve the application by allowing the processing time to be changed based on the items selected by the customer.  Also, I believe that the code could be altered to allow the application to run more efficiently.  
