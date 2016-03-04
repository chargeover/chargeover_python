import sys
import chargeover
import pprint

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

# Our package data
data = {
   
    "customer_id": 5,
    "holduntil_datetime": "2013-10-01",
    
    "line_items": [
        {
            "item_id": 239,
            "line_quantity": 15
        }
    ]
    }

# create a new recurring package
id = co.create('package', data)
if id is None:
    pprint.pprint(co.get_last_response())
    exit()
else:
    print("Our new recurring package ID is: " + str(id))
