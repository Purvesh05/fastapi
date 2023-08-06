from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item not found")
    
    
    hash_password = utils.hash(user.password)
    user.password = hash_password
    
    new_user = models.User(
        **user.model_dump()
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    return user
    