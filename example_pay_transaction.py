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

# Our data for the transaction
tdata = {
    "customer_id": 1,

    # You can optionally supply an amount (if you don't specify an amount, you MUST specify a list of invoice_id values -- the amount will be calculated for you)
    "amount": 18.62,
    
    # You can optionally supply a list of invoice_id values to apply this payment to
    "applied_to": [
        {
            "invoice_id": 24601
        }
    ]
}

# post a new transaction
id = co.create('transaction', tdata)

if id is None:
    pprint.pprint(co.get_last_response())
    exit()
else:
    print("Our transaction ID is: " + str(id))