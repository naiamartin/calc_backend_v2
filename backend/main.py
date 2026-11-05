from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import database, models
from backend.schemas import blog, user
from fastapi.middleware.cors import CORSMiddleware
import logging


logging.basicConfig(
    filename=Path(__file__).resolve().parent.parent / "server.log",
    encoding="utf-8",
    level=logging.DEBUG,
)

# Create all tables in the database
models.Base.metadata.create_all(bind=database.engine)

# Create the FastAPI application
app = FastAPI()

# Add CORS middleware to allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React's default port
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Dependency to get database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello, Microservice!"}


# CREATE - Add a new user
@app.post("/users/", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# READ - Get all users
@app.get("/users/", response_model=list[user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


# READ - Get a single user by ID
@app.get("/users/{user_id}", response_model=user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# UPDATE - Update an existing user
@app.put("/users/{user_id}", response_model=user.User)
def update_user(
    user_id: int,
    user: user.UserUpdate,
    db: Session = Depends(get_db),
):

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# DELETE - Remove a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


@app.get("/blogs/", response_model=list[blog.Blog])
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).offset(skip).limit(limit).all()
    return blogs


@app.post("/blogs/", response_model=blog.Blog)
def create_blog(blog: blog.BlogCreate, db: Session = Depends(get_db)):
    db_blog = models.Blog(**blog.model_dump())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


@app.get("/blogs/{blog_id}", response_model=blog.Blog)
def read_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@app.put(
    "/blogs/{blog_id}",
    response_model=blog.Blog,
)
def update_blog(
    blog_id: int,
    blog: blog.BlogUpdate,
    db: Session = Depends(get_db),
):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    for field, value in blog.model_dump(exclude_unset=True).items():
        setattr(db_blog, field, value)

    db.commit()
    db.refresh(db_blog)
    return db_blog


@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}
