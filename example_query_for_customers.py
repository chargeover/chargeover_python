import sys
import chargeover
import pprint 


''' AVAILABLE QUERY PARAMETERS
customer_id
bill_state
ship_state
bill_country
ship_country
external_key
token
company
superuser_id
superuser_email 
'''

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
cdata0 = {
	"name": "john",
	"email": "john@john.com",
	"id": "c-01"
}

# Our user/contact data 
cdata1 = {
	"name": "ron",
	"email": "ron@aol.com",
	"id": "c-02"
}

# Our user/contact data 
cdata2 = {
	"name": "ron",
	"email": "ron@ron.com",
	"id": "c-03"
}

# create a new card
id0 = co.create('customer', cdata0)
if id0 is None:
	pprint.pprint(co.get_last_response())

id1 = co.create('customer', cdata1)

if id1 is None:
    pprint.pprint(co.get_last_response())
    exit()
	
id2 = co.create('customer', cdata2)

if id2 is None:
    pprint.pprint(co.get_last_response())
    exit()

# Find a customer by query
where {'name': 'ron'}
customer = co.find("customer", where)
print "All customers matching search (in list)"
pprint.pprint(customer)