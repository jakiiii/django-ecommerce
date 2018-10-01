# Checkout Process

1. Cart -> Checkout View
	- Login / Register Or Entry an Email (as Guest)
	- Shipping Address
	- Billing Address
		- Billing Address
		- Creadit Card / Payment

2. Billing App / Component
	- Billing Profile
		- User or Email (Gust Email)
		- generate payment process token (Strip or Braintree)
    
3. Order / Invoice Component or App
    - Connect the Billing Profile
    - Shipping / Billing Address
    - Cart
    - Status -- Shipped or Cancelled