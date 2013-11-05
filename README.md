
ChargeOver Python API
=====================

This is a Python library for the [ChargeOver recurring billing platform](http://www.chargeover.com/). ChargeOver is a billing platform geared towards easy, automated, recurring invoicing. 


Use ChargeOver to:

* painlessly automate your recurring invoicing 
* allow your customers to log in to a customized portal to view and pay their bills online
* automatically follow up on late and missed payments
* build developer-friendly billing platforms (use the ChargeOver REST APIs, code libraries, webhooks, etc.)
* sync customer, invoice, and payment information to QuickBooks for Windows and QuickBooks Online


ChargeOver developer documentation:

* REST API: http://chargeover.com/docs/rest-api.html
* Webhooks: http://chargeover.com/docs/advanced/webhooks.html
* Example code: https://github.com/chargeover/chargeover_python/blob/master/CO_API_demo.py


ChargeOver developer account sign-up:

* https://chargeover.com/signup/


ChargeOver main documentation:

* http://chargeover.com/docs/


ChargeOver API access in other programming languages:

* https://github.com/chargeover/


Dependencies
------------

All imports should be standard python modules.

Other Notes
-----------

ChargeOver can be imported in interactive mode, interrogated with help(), and operated completely in the interactive interpreter. When
connecting, set the "interactive" named parameter to true to allow automatic pretty printing (CO method calls that support the named
parameter "pretty").

All of the JSON objects return are parsed into python dicts and lists.
