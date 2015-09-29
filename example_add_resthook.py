import sys
import chargeover
import pprint 

# For authentication, fill in these values from your ChargeOver
# server information under "Configuration -> API & Webhooks"
endpoint = 'http://dev.chargeover.com/signup/api/v3'
username = 'noECbNw0GDA7vtPLcuaVqJBRhUldjz38'
password = 'B6LnuVGE74Co1TacXxHjdwk9hKtPpIW0'
key_auth = False

co = chargeover.ChargeOver(
    endpoint, 
    username, 
    password, 
    key_auth = key_auth)

# Our resthook data (http://resthooks.org/)
data = {
    'target_url': 'http://playscape2.uglyslug.com/resthooks/customer_insert.php', 
    'event': 'customer.insert'
    }

# Create a new resthook
id = co.create('_resthook', data)
if id is None:
    pprint.pprint(co.get_last_response())
    exit()
else:
    print("Our new Rest Hook ID is: " + str(id))