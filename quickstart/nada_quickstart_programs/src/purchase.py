from nada_dsl import *

def nada_main():
	
	merchant = Party("Merchant") # initializing a 'merchant' party
	
	inventory = setInventory(merchant) # the 'merchant' setting the inventory
	
	orderId = PublicInteger(0); # creating an orderId element
	
	customer = Party("Customer") # initializing a 'customer' party
	
	order = makeOrder(customer, inventory, orderId) #customer placing an 'order'
	
	bill = processOrder(order, customer) # fetching the bill for the customer's order
	
	return(Output(bill,"bill_receipt",customer))
	
# allowing the 'party00' to set up their 'inventory' list
def setInventory(party00: Party):
	
	inventory = [] # initializing an empty list of inventory
	
	# 'merchant' party setting the no.of inventory to enter
	noOfItems = PublicInteger(Input(name="no_of_items", party=party00))
	
	# creating an 'item' tuple and appending to the inventory list
	for i in range(noOfItems):
		item = createItem(party00)
		inventory.append(item)
	
	return (Output(inventory,"inventory_list",party00)) # returns inventory list

# allowing the 'party00' to create an 'item' tuple
def createItem(party00: Party):
	
	itemId = PublicInteger(Input(name="item_id", party=party00)) # item identifier as a public integer input
	itemPrice = PublicInteger(Input(name="item_price", party=party00)) # item unit price as a public integer input
	itemQty = PublicInteger(Input(name="item_qty", party=party00))# item quantity as a public integer input
	
	item = (itemId, itemPrice, itemQty) # creating an item tuple
	
	return(Output(item,"item_element",party00))

#allwoing the 'party00' to create an 'order' from the 'inventory'
def makeOrder(party00: Party, inventory00: List, orderId00: PublicInteger):
	
	orderNo = orderId00 + Integer(1) #incrementing the orderid for all new orders
	
	order = [orderNo] #initilizing 'order' as a list with its first element as orderNo.
	
	# for each 'item' in the 'inventory', defining an 'orderEl' tuple
	for item in inventory00:
		itemSrNo = item[0] #itemId as 'itemSrNo'
		units = Integer(0) # no.of units to purchase, initialised as Integer(0)

		# if the item quantity avaialble in the inventory is greater than  Integer(0)
		units = (item[2] > Integer(0)).if_else(
			SecretInteger(Input(name="purchase_qty", party=party00)), # accepting a SecretInteger input of no.of units to purchase
			Integer(0)
		)
		
		orderEl = (itemSrNo,units) # creating the order tupule for the specific item
		
		order.append(orderEl) # appending the orderEl corresponding to the item, to 'order'
	
	return (Output(order,"order_list",party00))

# processing the 'order00' to fetch the final bill
def processOrder(order00: List, inventory00:List, party00: Party):
	
	orderLength = len(order00) #length of order list
	
	orderNo = order00[0] # order number - the first element of order list
	
	orderCost = Integer(0) # initialising the total cost for thr order as Integer(0)
	
	for i in range(1,orderLength): #for each orderEl tupules in the 'order' list
		n = order00[i][0] # fetching the itemSrNo, which is equivalent to the corresponding itemID in the 'inventory' list
		
		purchaseQty = order00[i][1] #no.of units to purchase
			
		itemPurchaseCost = (purchaseQty > Integer(0)).if_else( # verifying wether to purchase any unit or not 
			(purchaseQty < inventory00[n][2]).if_else( # verifying if the purchase quantity is less than that which is available in the 'inventory'
				purchaseQty * inventory00[n][1] , Integer(0) # caluating the price for the particular item
			),Integer(0)
		)
		
		orderCost = orderCost + itemPurchaseCost #incrementing the 'ordercost' for each 'item'
		
	bill = (orderNo, orderCost) #a bill tuple with the order no and total cost of the order
	
	return (Output(bill,"bill_receipt",party00))