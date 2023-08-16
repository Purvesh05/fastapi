from typing import List
from app import schemas, models
import pytest

def test_get_all_posts(authorized_client, test_posts):

    res = authorized_client.get("/posts/")
    

    def validate(posts):
        return schemas.PostVote(**posts)

    post_map = map(validate,res.json())
    posts = list(post_map)
    

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts")
    
    assert res.status_code == 401

def test_unauthorized_user_get_one_pos (client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client):
    res = authorized_client.get(f"/posts/433442")
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = schemas.PostVote(**res.json())

    assert post.Post.id  == test_posts[0].id
    assert post.Post.content  == test_posts[0].content


@pytest.mark.parametrize("title, content, published",[
    ("title 1","content 1", True),
    ("title 2","content 2", False),
    ("title 3","content 3", True),
    ("title 4","content 4", False)
      ])
def test_create_post(authorized_client,test_user,title, content, published ):
   
    res = authorized_client.post("/posts",json={"title": title , "content":content,"published":published})
    post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert post.user_id == test_user['id']
    assert post.title == title
    assert post.content == content
    assert post.published == published

def test_create_post_default_published_true(authorized_client,test_user ):
    res = authorized_client.post("/posts",json={"title": "title" , "content":"content"})
    post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert post.user_id == test_user['id']
    assert post.title == "title"
    assert post.content == "content"
    assert post.published == True


def test_unauthorized_create_post (client):
    res = client.post("/posts",json={"title": "title" , "content":"content","published":False})
    assert res.status_code == 401


def test_delete_post(authorized_client,test_posts ):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_unauthorized_delete_post (client,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_delete_post_not_exist(authorized_client):
    res = authorized_client.delete(f"/posts/2321231")
    assert res.status_code == 404
  

# with creating a new post with different user
def test_delete_other_user_post(authorized_client1,test_posts ):
    
    res = authorized_client1.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 403

# with creating different user with old post
def test_delete_other_user_post1(authorized_client,test_posts ):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client,test_posts ):

    res = authorized_client.put(f"/posts/{test_posts[0].id}",json={"title": "title" , "content":"content","published":False})
    post = schemas.Post(**res.json())

    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content
    assert post.published == test_posts[0].published
    assert post.user_id == test_posts[0].user_id
    assert res.status_code == 205

def test_unauthorized_update_post (client,test_posts):
    res = client.put(f"/posts/{test_posts[0].id}",json={"title": "title" , "content":"content","published":False})
    assert res.status_code == 401
    
def test_update_post_not_exist(authorized_client):
    res = authorized_client.put(f"/posts/2321231",json={"title": "title" , "content":"content","published":False})
    assert res.status_code == 404

# with creating a new post with different user
def test_update_other_user_post(authorized_client1,test_posts ):
    res = authorized_client1.put(f"/posts/{test_posts[0].id}",json={"title": "title" , "content":"content","published":False})
    assert res.status_code == 403

# with creating different user with old post
def test_update_other_user_post1(authorized_client,test_posts ):
    res = authorized_client.put(f"/posts/{test_posts[3].id}",json={"title": "title" , "content":"content","published":False})
    assert res.status_code == 403