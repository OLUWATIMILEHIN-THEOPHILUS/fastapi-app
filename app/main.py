from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

@app.get("/")
def home():
    return {"data": "Home Page"}

############## CODES FOR DUMMY DATABASE #####################

#CREATING MODEL USING PYDANTIC
# class Product(BaseModel):
#     id: Optional[int] = None
#     name: str
#     description: str
#     price: float
#     quantity: int
#     on_sales: bool = True
#     ratings: Optional[float] = None

#MODEL TO ENABLE UPDATING A POST WITH PATCH 
class Product(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    on_sales: Optional[bool] = True
    ratings: Optional[float] = None

#DUMMY DATABASE FOR PRODUCTS

my_database = [
    {
        "id": 1,
        "name": "Sneakers",
  "description": "Skechers Men's Sneakers",
  "price": 20.5,
  "quantity": 3,
  "on_sales": 0,
  "ratings": 4.0
    },
    {
        "id": 2,
        "name": "T-Shirt",
  "description": "Nike Men's T-Shirt",
  "price": 15,
  "quantity": 5,
  "on_sales": 1,
  "ratings": 4.5
    }
]


############## FUNCTIONS AND LOGICS #####################

def find_product(id):
    for p in my_database:
        if p["id"]==id:
            return p

def get_product_index(id):
    for i, p in enumerate(my_database):
        if p["id"]==id:
            return i

############## ENDPOINTS FOR DUMMY DATABASE #####################

@app.get("/products")
def get_products():
    return {"data": my_database} 


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: Product = Body(...)):
    product_dict = product.dict()
    product_dict["id"] = randrange(1, 123456789)
    my_database.append(product_dict)
    return {"message": "Product has been created successfully!", "data": product_dict, "status": status.HTTP_201_CREATED}


@app.get("/products/latest")
def get_latest_product():
    product = my_database[len(my_database)-1]
    return {"data": product}


# Get a product using query parameter

# @app.get("/products/")
# def get_product(q: int = None):
#     product = find_product(q)
#     if product is not None:
#         return {"data": product}
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id: {q} was not found")


# Get a product by id

@app.get("/products/{id}")
def get_product(id: int):
    product = find_product(id)
    if product is not None:
        return {"data": product}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id: {id} was not found")


# Delete a product using .remove()

@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    product = find_product(id)
    if product is not None:
        my_database.remove(product)
        return {"message": "Product has been deleted successfully!", "status": status.HTTP_204_NO_CONTENT}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exist")


# Delete a product using .pop()

# @app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_product(id: int):
#     index = get_product_index(id)
#     if index is not None:
#         my_database.pop(index)
#         return {"message": "Product has been deleted successfully!", "status": status.HTTP_204_NO_CONTENT}
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exist")


# Edit a post using PUT

# @app.patch("/edit/{id}")
# def edit_product(id: int, product: Product = Body(...)):
#     product_dict = product.dict()
#     product_dict["id"] = id
#     product = get_product_index(id)
#     if product is not None:
#         my_database[product] = product_dict
#         return {"data": product_dict, "message": "Product has been updated successfully", "status": status.HTTP_200_OK}
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exist")



# ENDPOINT TO ENABLE UPDATING A POST WITH PATCH 

@app.patch("/edit/{id}")
def edit_product(id: int, product: Product = Body(...)):
    product_dict = product.dict(exclude_unset=True)
    product_dict["id"] = id
    product = get_product_index(id)
    if product is not None:
        product_data = my_database[product]
        product_data.update(product_dict) 
        my_database[product] = product_data 
        return {"data": product_data, "message": "Product has been updated successfully", "status": status.HTTP_200_OK}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exist")