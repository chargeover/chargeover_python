import sys
import chargeover
import pprint 

# For authentication, fill in these values from your ChargeOver
# server information under "Configuraion->API and Webhooks"
endpoint = 
username = 
password = 

# Set this to True to use "COv1 Signature" authorization
key_auth = False

co = chargeover.ChargeOver(
    endpoint, 
    username, 
    password, 
    key_auth = key_auth)

# Our customer data 
data = {
    'company': "My Test Python Company",
    
    'bill_addr1': "72 E Blue Grass Road",
    'bill_addr2': "Suite D", 
    'bill_city': "Willington", 
    'bill_state': "CT",
    'bill_postcode': "06279",

    'superuser_name': "Keith Palmer",
    'superuser_email': "test@test.com"
    }

# Create a new customer
id = co.create('customer', data)
if id is None:
    pprint.pprint(co.get_last_response())
    exit()
else:
    print("Our new customer ID is: " + str(id))