from fastapi import FastAPI, Body, HTTPException, status, Depends, APIRouter
from fastapi import status
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/user", 
    tags=["User"]
)

@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter_by(id=id)
    user = user_query.first()
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id ({id}) was not found")
    return user

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    user_query = db.query(models.User)
    users = user_query.all()
    return users