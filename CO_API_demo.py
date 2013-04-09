import sys
import chargeover
import pprint # pretty printer

# For authentication, fill in these values from your ChargeOver
# server information under "Configuraion->API and Webhooks"
endpoint = 
username = 
password = 

# set this to True to use "COv1 Signature" authorization
key_auth = True

co = chargeover.ChargeOver(endpoint, username, password, 
                           key_auth = key_auth)

sendable = {
    'company':"A COAPI Co.",
    'email':"COAPI@chargeover.notreal",
    'external_key':"ourcustomer-01"
}

# create a new customer
id = co.create("customer", sendable)
if id is None:
    pprint.pprint(co.get_last_response())
    exit()

# Usually if create fails its because the customer already exists. 

# Find a customer by id
cust = co.find_by_id("customer", id)
print "Customer just created:"
pprint.pprint(cust)

# Find a customer by query
where = {'external_key':"ourcustomer-01"}
cust = co.find("customer", where)
print "All customers matching search (it's a list!)"
pprint.pprint(cust)

# Update our customer
sendable = cust[0]
print "Changing external key"
sendable['external_key'] = "ourcustomer-02"
try:
    id = co.update("customer", sendable['customer_id'], sendable)
except:
    print co._http_res
    print co._content

if id is None:
    pprint.pprint(co.get_last_response())
    sys.exit("update failed")

# And find the updated customer
cust = co.find_by_id("customer", id)
print "Updated customer"
pprint.pprint(cust)
