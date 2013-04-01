import sys
import chargeover
import pprint # pretty printer

# For basic authentication, fill in these values from your ChargeOver
# server information under "Configuraion->API and Webhooks"
endpoint = ""
username = ""
password = ""

co = chargeover.ChargeOver(endpoint, username, password)

sendable = {
    'company':"A COAPI Co.",
    'email':"COAPI@chargeover.notreal",
    'external_key':"ourcustomer-01"
}

# create a new customer
id = co.create("customer", sendable)
if id is None:
    pprint.pprint(co.get_last_response())

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
id = cust[0]['customer_id']
print "Changing external key"
sendable['external_key'] = "ourcustomer-02"
id = co.update("customer", id, sendable)
if id is None:
    pprint.pprint(co.get_last_response())
    sys.exit("update failed")

# And find the updated customer
cust = co.find_by_id("customer", id)
print "Updated customer"
pprint.pprint(cust)
