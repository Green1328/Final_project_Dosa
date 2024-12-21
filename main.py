from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel

#create a model, building off of base model (Pydantic model)
class Customer(BaseModel):
    name: str
    phone: str

class Item(BaseModel):
    name: str 
    price: float

class Order(BaseModel):
    timestamp: int 
    cust_id: int
    notes: str


#Request Body
#When you need to send data from client(browser) to your API, 
#you send it as a request body
#request body is data sent by the client to your API
#Reponse body is the data your API sends to the client
def db_setup():
    conn = sqlite3.connect("db.sqlite")
    return (conn, conn.cursor())
  
app = FastAPI()

#customer
@app.get("/customers/{customer_id}")
def read_customer(customer_id: int):
    conn, cursor= db_setup()
    cursor.execute( "SELECT * FROM customers WHERE id=?;", (customer_id,))
    row= cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return {
        "id": row[0],
        "name": row[1],
        "phone": row[2]
    }


#customers delete
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    conn, cursor = db_setup()
    cursor.execute("DELETE FROM customers WHERE id= ?;", (customer_id,))
    conn.commit()
    rows_affected= cursor.rowcount
    conn.close()
    return {"rows_affected": rows_affected}

#customers add new
@app.post("/customers")
def create_customer(customer: Customer):
    conn, cursor= db_setup()
    cursor.execute("INSERT INTO customers (name,phone) VALUES (?,?);", (customer.name, customer.phone))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {
        "id": new_id,
        "name": customer.name,
        "phone": customer.phone
    }

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: Customer):
    conn, cursor = db_setup()
    cursor.execute("UPDATE customers SET name=?, phone=? WHERE id=?;", (customer.name, customer.phone, customer_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Customer not found or no changes made.")
    return {"rows_affected": rows_affected}



#items
@app.get("/items/{item_id}")
def read_item(item_id: int):
    conn, cursor = db_setup()
    cursor.execute("SELECT * FROM items WHERE id=?;", (item_id,))
    row= cursor.fetchone()
    conn.close()
    return {
        "id": row[0],
        "name": row[1],
        "price": row[2]
    }

#item delete
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn, cursor = db_setup()
    cursor.execute("DELETE FROM items WHERE id=?;", (item_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return {"rows_affected": rows_affected}


#item create
@app.post("/items")
def create_item(item: Item):
    conn, cursor =db_setup()
    cursor.execute("INSERT INTO items(name,price) VALUES (?,?);", (item.name, item.price))
    conn.commit()
    new_id=cursor.lastrowid
    conn.close()
    return {
        "id": new_id,
        "name": item.name,
        "price": item.price
    }

#item update
@app.put("/items/{item_id}")
def update_item(item_id:int, item: Item):
    conn, cursor= db_setup()
    cursor.execute("UPDATE items SET name =?, price=? WHERE id=?;", (item.name, item.price, item_id))
    conn.commit()
    rows_affected=cursor.rowcount
    conn.close()
    return {"rows_affected": rows_affected}



#orders
@app.get("/orders/{order_id}")
def read_order(order_id: int):
    conn, cursor= db_setup()
    cursor.execute("SELECT * FROM orders WHERE id=?;", (order_id,))
    row= cursor.fetchone()
    conn.close()
    return {
        "id": row[0],
        "timestamp": row[1],
        "cust_id": row[2],
        "notes": row[3]
    }

@app.delete("/orders/{order_id}")
def delete_order(order_id:int):
    conn, cursor = db_setup()
    cursor.execute("DELETE FROM item_list WHERE order_id=?;", (order_id,))
    cursor.execute("DELETE FROM orders WHERE id=?;", (order_id,))
    conn.commit()       
    rows_affected=cursor.rowcount
    conn.close       
    return { "rows_affected": rows_affected}


@app.post("/orders")
def create_order(order: Order):
    conn, cursor= db_setup()
    cursor.execute("INSERT INTO orders (timestamp,cust_id,notes) VALUES (?,?,?);", (order.timestamp, order.cust_id, order.notes))
    conn.commit()
    new_id= cursor.lastrowid
    conn.close()
    return {
        "id": new_id,
        "timestamp": order.timestamp,
        "cust_id": order.cust_id,
        "notes": order.notes
    }

@app.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    conn, cursor = db_setup()
    cursor.execute("""
        UPDATE orders
        SET timestamp = ?, cust_id = ?, notes = ?
        WHERE id = ?;
    """, (order.timestamp, order.cust_id, order.notes, order_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Order not found or no changes made.")
    return {"rows_affected": rows_affected}
