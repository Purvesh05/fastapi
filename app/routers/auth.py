from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, utils,oauth2
from ..database import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/login', status_code=status.HTTP_200_OK,response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
    
    # print( "user_credentials: ", user_credentials.password )

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User not Found")
    
    if not utils.verify(plain_password=user_credentials.password,hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
     
    access_token = oauth2.create_acces_token(data={"user_id":user.id})
    return {"access_token": access_token, "token_type": "bearer"}