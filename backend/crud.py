from sqlalchemy.orm import Session
from sqlalchemy import or_
import models, schemas
from auth_utils import get_password_hash

# User CRUD operations
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Blog CRUD operations
def get_blogs(db: Session, skip: int = 0, limit: int = 10, category: str = None, tag: str = None):
    query = db.query(models.Blog).filter(models.Blog.published == True)
    
    if category:
        query = query.join(models.Category).filter(models.Category.name == category)
    
    if tag:
        query = query.join(models.Blog.tags).filter(models.Tag.name == tag)
    
    return query.offset(skip).limit(limit).all()

def get_blog(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

# In crud.py
def create_blog(db: Session, blog_data: dict, tags: list, author_id: int):
    # Get or create tags
    tag_objects = []
    for tag_name in tags:
        tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tag_objects.append(tag)
    
    # Create blog
    db_blog = models.Blog(**blog_data, author_id=author_id)
    db_blog.tags = tag_objects
    
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def update_blog(db: Session, blog_id: int, blog_data: dict):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog:
        for key, value in blog_data.items():
            setattr(db_blog, key, value)
        db.commit()
        db.refresh(db_blog)
    return db_blog

def delete_blog(db: Session, blog_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog:
        db.delete(db_blog)
        db.commit()
    return db_blog

# Comment CRUD operations
def get_comments_by_blog(db: Session, blog_id: int):
    return db.query(models.Comment).filter(models.Comment.blog_id == blog_id).all()

def get_comment(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def create_comment(db: Session, comment_data: schemas.CommentCreate, author_id: int, blog_id: int):
    db_comment = models.Comment(**comment_data.dict(), author_id=author_id, blog_id=blog_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment

# Like CRUD operations
def get_like(db: Session, user_id: int, blog_id: int):
    return db.query(models.Like).filter(
        models.Like.user_id == user_id, 
        models.Like.blog_id == blog_id
    ).first()

def create_like(db: Session, user_id: int, blog_id: int):
    db_like = models.Like(user_id=user_id, blog_id=blog_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

def delete_like(db: Session, user_id: int, blog_id: int):
    db_like = get_like(db, user_id=user_id, blog_id=blog_id)
    if db_like:
        db.delete(db_like)
        db.commit()
    return db_like

# Category CRUD operations
def get_categories(db: Session):
    return db.query(models.Category).all()

def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category