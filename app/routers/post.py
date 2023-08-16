from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
#from sqlalchemy.sql.functions import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)

@router.get("/",response_model=List[schemas.PostVote])
def post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post, ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # if posts == []:
    #     raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"No Post from {current_user.email}")
    
    # .filter(models.Post.title.contains(search)).limit(limit).offset(skip)

    result_query = db.query(models.Post,func.count(models.Post.id).label("votes")).join(models.Vote,\
                    models.Post.id == models.Vote.post_id,isouter=True).\
                    group_by(models.Post.id).filter(models.Post.title.contains(search)).\
                    limit(limit).offset(skip)
    # print(result_query)
    result = result_query.all()
    # print(result)
    return result
   


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post_dict = post.dict() 
    # post_dict['id'] = randrange(0,1000)
    # my_posts.append(post_dict)

    # cursor.execute(""" INSERT INTO posts(title, content, publishedz))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print("current_user: ",current_user.id )
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
 
    new_post = models.Post(
        user_id=current_user.id,
        **post.model_dump() ## dict funtion is replaced ny model_dump
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post) # not printing the result or returning the objects

    return new_post


@router.get("/{id}",response_model=schemas.PostVote)
def get_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user )):

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s;""", [id] )
    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post,func.count(models.Post.id).label("votes")).join(models.Vote,\
                    models.Post.id == models.Vote.post_id,isouter=True).\
                    group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user )):
    
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *; """, [id] )
    # post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if not post:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden not owner post")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT,response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user )):

    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *;""", (post.Title,post.content,post.published,id) )
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden not owner post")
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()  
    
    return post_query.first()
