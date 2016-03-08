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

# Our user/contact data 
data = {
    'customer_id': 71,    # This is the customer id # this card should be attached to

    'number': "1234 5678 9101 1121", 
    'expdate_year': '2017',
    'expdate_month': '05', 
    'phone': '616-867-5309',
    'name': 'Bob Dobbs',
    'address': '123 E TheWay Drive',
    'city': 'Chicago',
    'state': 'IL',
    'postcode': '60606',
    'country': 'United States'
    }

# create a new card
id = co.create('creditcard', data)
if id is None:
    pprint.pprint(co.get_last_response())
    exit()
else:
    print("Our new creditcard ID is: " + str(id))
