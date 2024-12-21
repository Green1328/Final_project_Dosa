# Final project Dosa Restaurant
This project provides a REST API backend for our Dosa Restaurant.
This project uses:
1. **SQLite** database
2. **Fast API** to provide ascces to customers,items,orders
3. **Pydantic models**
4. **example_orders.json**

The API supports CRUD (create,read, update, delete) for the three main objects (customers, items, orders)

The init_db.py initializes an empty database using relational constraints (primary keys and foreign keys) from the example_orders.json file

The main.py file is the main FastAPI application where we create the following endpoints for customers, items, and orders. 
1. **POST**
2. **GET**
3. **DELETE**
4. **PUT**
