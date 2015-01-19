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
    'chargeoverjs_token': 'abcd5678'
    }

# Create a new customer
id = co.create('_config', data)
if id is None:
    pprint.pprint(co.get_last_response())
    exit()
else:
    print("Updated config!")