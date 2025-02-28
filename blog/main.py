# fastapi imports
from fastapi import FastAPI, Depends, status, HTTPException

# database  imports
from . import schemas, models
from .dbconfig import engine, SessionLocal
from sqlalchemy.orm import Session

# password imports
from .hashing import Hash

# pydantic imports
from pydantic import List

# Creating the tables in the database based on the models in models.py file
models.Base.metadata.create_all(engine)

app = FastAPI()

# connection with database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ** BLOG METHODS **

# === POST ===
@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)): # create a blog

    newblog = models.Blog(title=request.title, body=request.body)
    db.add(newblog)
    db.commit()
    db.refresh(newblog)
    return newblog


# === DELETE ===
@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def destroy_blog(id, db: Session = Depends(get_db)): # delete by id
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with ID {id} is not available'
            )

    blog.delete(synchronize_session=False)

    db.commit()
    return f'Blog with ID {id} was deleted  :)'


# === PUT ===
@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)): # update by id
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with ID {id} is not available'
            )
    blog.update(request.model_dump())
    db.commit()
    return f'Blog with ID {id} was updated'


# === GET ===
@app.get('/blogs', tags=['blogs'], request_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db)): # get all blogs from database

    blogs = db.query(models.Blog).all()

    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'No blogs in database'
        )
    
    return blogs


@app.get('/blog/{id}',tags=['blogs'], request_model=schemas.ShowBlog)
def get_blog_by_id(id, db: Session = Depends(get_db)): # get blog by id
    
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with ID {id} is not available'
        )
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'details': f'Blog with ID {id} is not available'}
    return blog


# ** USER METHODS **


# === POST ===
@app.post('/user', status_code=status.HTTP_201_CREATED, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)): # create an user
    
    newuser = models.User(
        name=request.name, 
        email=request.email, 
        password=Hash.bcrypt(request.password)
    )
    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser

# === DELETE ===
@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
def destroy_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with ID {id} is not available'
            )

    user.delete(synchronize_session=False)

    db.commit()
    return f'User with ID {id} was deleted  :)'


# === PUT ===
@app.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['users'])
def update_user(id, request: schemas.Blog, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with ID {id} is not available'
            )
    user.update(request.model_dump())
    db.commit()
    return f'User with ID {id} was updated'

# === GET ===
@app.get('/users', tags=['users'], response_model=List[schemas.ShowUser])
def all_users(db: Session = Depends(get_db)): # get all users from database
    users = db.query(models.User).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'No users in database'
        )
    
    return users

@app.get('/user/{id}', tags=['users'], response_model=schemas.ShowUser)
def get_user_by_id(id, db: Session = Depends(get_db)): # get user by id
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with ID {id} is not available'
        )
    return user