from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


@app.get("/")
def home():
    return {"data": "Home Page"}


class Product(BaseModel):
    name: str
    price: float
    description: Optional [str] = None
    inventory: Optional [int] = None
    on_sales: Optional [bool] = False


try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='5176', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connection to database was successful!")
except Exception as error:
    print("Connection to database failed!")
    print(f"Error: {error}" )



@app.get("/products", status_code=status.HTTP_200_OK)
def get_products():
    cursor.execute("SELECT * FROM products;")
    products = cursor.fetchall()
    return {"data": products}


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product = Body(...)):
    cursor.execute("INSERT INTO products (name, price, description, inventory, on_sales) VALUES (%s, %s, %s, %s, %s) RETURNING *", (product.name, product.price, product.description, product.inventory, product.on_sales))
    cursor.connection.commit()
    product = cursor.fetchone()
    return({"message": "Product has been created successfully!", "data": product, "status": status.HTTP_201_CREATED})


@app.get('/products/{id}', status_code=status.HTTP_200_OK)
def get_product(id: int):
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cursor.fetchone()
    if product is not None:
        return({"data": product})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id ({id}) was not found")


@app.put('/products/{id}', status_code=status.HTTP_200_OK)
def update_product(id: int, product: Product = Body(...)):
    cursor.execute("UPDATE products SET name = %s, price = %s, description = %s, inventory = %s, on_sales = %s WHERE id = %s RETURNING *", (product.name, product.price, product.description, product.inventory, product.on_sales, id))
    cursor.connection.commit()
    product = cursor.fetchone()
    if product is not None:
        return({"message": "Product updated successfully!", "data": product, "status": status.HTTP_200_OK})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id ({id}) was not found")


@app.delete('/products/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    cursor.execute("DELETE FROM products WHERE id = %s RETURNING *", (id,))
    product = cursor.fetchone()
    if product is not None:
        cursor.connection.commit()
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id ({id}) does not exist")