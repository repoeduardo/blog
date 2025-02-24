# fastapi imports
from fastapi import FastAPI, Depends, status, HTTPException

# database  imports
from . import schemas, models
from .dbconfig import engine, SessionLocal
from sqlalchemy.orm import Session

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

# === POST ===

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)): # create a blog

    newblog = models.Blog(title=request.title, body=request.body)
    db.add(newblog)
    db.commit()
    db.refresh(newblog)
    return newblog


# === GET ===

@app.get('/')
def index():
    return {'msg':'index page'}

@app.get('/blogs')
def all_blogs(db: Session = Depends(get_db)): # get all blogs from database

    blogs = db.query(models.Blog).all()

    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'No blogs in database'
        )
    
    return blogs


@app.get('/blog/{id}')
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