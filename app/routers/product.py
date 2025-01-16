from fastapi import FastAPI, Body, HTTPException, status, Depends, APIRouter
from fastapi import status
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/products",
    tags=["Product"]
)

@router.get("/my_products", status_code=status.HTTP_200_OK, response_model=schemas.ProductsListResponse)
def get_products_for_current_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 5):
    product_query = db.query(models.Product).filter_by(user_id=current_user.id)
    products = product_query.limit(limit).all()
    return schemas.ProductsListResponse(count=len(products), products=products)


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.ProductsListResponse)
def get_products(db: Session = Depends(get_db), limit: int = 5, skip: int = 0, search: str = ""):
    products = db.query(models.Product).filter(models.Product.name.icontains(search)).limit(limit).offset(skip).all()
    return schemas.ProductsListResponse(count=len(products), products=products)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_product = models.Product(user_id=current_user.id, **product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ProductResponse)
def get_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    product = db.query(models.Product).filter_by(id=id).first()
    if product is not None:
        return product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id ({id}) was not found")


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ProductResponse)
def update_product(id: int, updated_product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    product_query = db.query(models.Product).filter_by(id=id)
    product = product_query.first()
    if product is not None:
        if product.user_id == current_user.id:
            product_query.update(updated_product.dict())
            db.commit()
            db.refresh(product)
            return product
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id ({id}) was not found")


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    product_query = db.query(models.Product).filter_by(id=id)
    product = product_query.first()
    if product is not None:
        if product.user_id == current_user.id:
            product_query.delete(synchronize_session=False)
            db.commit()
            return({"status": status.HTTP_204_NO_CONTENT})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with the id ({id}) does not exist")
