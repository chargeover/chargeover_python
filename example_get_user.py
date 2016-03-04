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


cdata = {
	
	'company': "Acme Inc.",
	'email': 'csmith@acme.co',
	'external_key': "cid001"
	
}

id = co.create("customer", cdata)
if id is None:
	pprint.pprint(co.get_last_response())
	exit()

# Find a customer by id
cust = co.find_by_id("customer", id)
print "Customer from specified id"
pprint.pprint(cust)


# Find a customer by query
where {'external_key': 'cid001'}
customer = co.find("customer", where)
print "All customers matching search (in list)"
pprint.pprint(customer)