import sys
import chargeover
import pprint 

# For authentication, fill in these values from your ChargeOver
# server information under "Configuraion->API and Webhooks"
endpoint = "http://dev.chargeover.com/signup/api/v3.php"
username = "7sutWFEO2zKVYIGmZMJ3Nij5hfLxDRb8"
password = "9vCJbmdZKSieVchyrRItFQw8MBN4lOH3"

# Set this to True to use "COv1 Signature" authorization
key_auth = False

co = chargeover.ChargeOver(
    endpoint, 
    username, 
    password, 
    key_auth = key_auth)

# Our user/contact data 
data = {
    'customer_id': 71,    # This is the customer id # this contact should be attached to

    'name': 'Shannon B Palmer', 
    'email': 'shannon@test.com', 
    'phone': '860-634-1602'
    }

# create a new customer
id = co.create('user', data)
if id is None:
    pprint.pprint(co.get_last_response())
    exit()
else:
    print("Our new user ID is: " + str(id))