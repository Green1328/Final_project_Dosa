#script that will initialize an empty database using relational contraints
#(primary keys and foreign keys) from example_osrders.json file
import sqlite3
import json

connection = sqlite3.connect("db.sqlite")
cursor = connection.cursor()

#create customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
	id INTEGER PRIMARY KEY,  
	name CHAR(64) NOT NULL,
	phone CHAR(10) NOT NULL
);
""")

#create items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS items(
	id INTEGER PRIMARY KEY,
	name CHAR(64) NOT NULL,
	price REAL NOT NULL
);
""")

#create orders table with foreign key to customers
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
	id INTEGER PRIMARY KEY,
	timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	cust_id INT NOT NULL,
    notes TEXT,
    FOREIGN KEY(cust_id) REFERENCES customers(id)
);
""")

#Create item_list table linking orders and items
cursor.execute("""
CREATE TABLE IF NOT EXISTS item_list(
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES items(id)
);
""")

#read the JSON file
with open('example_orders.json', 'r') as file:
    data = json.load(file)

#go through each customer in the order
customers={}
for order in data:
    name = order['name']
    phone = order['phone']
    customers[phone] = name

#insert each customer into the customers table
for (phone, name) in customers.items():
    cursor.execute("INSERT INTO customers (name,phone) VALUES (?,?);", (name, phone)) 
  
#Go through each order items and pull out the unique ones
items ={}
for order in data:
    for it in order['items']:
        i_name =it['name']
        i_price =it['price']
        items[i_name] = i_price

#insert each unique item into the items table
for (i_name, i_price) in items.items():
    cursor.execute("INSERT INTO items (name,price) VALUES (?,?);", (i_name, i_price)) 
  
#Insert into orders table and item_list table 
for order in data:
    phone =order['phone']
    timestamp = order['timestamp']
    notes = order['notes']
    #get the customer id
    res = cursor.execute("SELECT id FROM customers WHERE phone= ?;", (phone,))
    cust_id = res.fetchone()[0] 
    #insert into orders
    cursor.execute("INSERT INTO orders (timestamp, cust_id, notes) VALUES(?,?,?)", (timestamp, cust_id, notes))
    order_id = cursor.lastrowid
    #insert into item_list for each item in the order
    for it in order['items']: 
        i_name = it['name']
        res_item = cursor.execute("SLECT id FROM items WHERE name=?;", (i_name,))
        item_id =res_item.fetchone()[0]
        cursor.execute("INSERT INTO item_list(order_id, item_id) VALUES (?,?);", (order_id,item_id))

connection.commit()
connection.close()
