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
    'customer_id': 3, 
    'invoice_date': '2014-03-05', 
    'line_items': [
            {
                'item_id': 5, 
                'line_rate': 25.95, 
                'line_quantity': 3
            },
            {
                'item_id': 3, 
                'line_rate': 15.95, 
                'line_quantity': 1
            }
        ]
    }

# create a new customer
id = co.create('invoice', data)
if id is None:
    pprint.pprint(co.get_last_response())
    exit()
else:
    print("Our new invoice ID is: " + str(id))