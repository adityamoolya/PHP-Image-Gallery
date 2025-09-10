from fastapi import APIRouter, Depends, HTTPException, Response, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
import os
import markdown
from datetime import datetime

import schemas, crud
from database import get_db
from auth_utils import get_current_active_user

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)

# Get all blogs with filtering and pagination
@router.get("/", response_model=List[schemas.Blog])
def get_blogs(
    skip: int = 0, 
    limit: int = 10, 
    category: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_blogs(db, skip=skip, limit=limit, category=category, tag=tag)

# Get single blog
@router.get("/{blog_id}", response_model=schemas.Blog)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Increment view count
    db_blog.views += 1
    db.commit()
    db.refresh(db_blog)
    
    return db_blog

# Create blog with file upload support
# In routers/blog.py
@router.post("/", response_model=schemas.Blog)
def create_blog(
    title: str = Form(...),
    content: str = Form(...),
    content_type: str = Form("text"),
    content_format: str = Form("text"),
    published: bool = Form(True),
    category_id: Optional[int] = Form(None),
    tags: List[str] = Form([]),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    # Handle file upload if present
    media_content = None
    media_filename = None
    media_type = None
    
    if file and content_type in ["photo", "video", "audio", "uploader"]:
        # Read file content
        media_content = file.file.read()
        media_filename = file.filename
        media_type = file.content_type
    
    # Process markdown if needed
    if content_format == "markdown":
        content = markdown.markdown(content)
    
    # Create blog
    blog_data = {
        "title": title,
        "content": content,
        "content_type": content_type,
        "content_format": content_format,
        "published": published,
        "category_id": category_id,
        "media_content": media_content,
        "media_filename": media_filename,
        "media_type": media_type
    }
    
    return crud.create_blog(db=db, blog_data=blog_data, tags=tags, author_id=current_user.id)


# Update blog
@router.put("/{blog_id}", response_model=schemas.Blog)
def update_blog(
    blog_id: int,
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Check if user is author or admin
    if db_blog.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.update_blog(db=db, blog_id=blog_id, blog_data=blog.dict())

# Delete blog
@router.delete("/{blog_id}")
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Check if user is author or admin
    if db_blog.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    crud.delete_blog(db=db, blog_id=blog_id)
    return {"message": "Blog deleted successfully"}

# Like a blog
@router.post("/{blog_id}/like")
def like_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Check if user already liked this blog
    existing_like = crud.get_like(db, user_id=current_user.id, blog_id=blog_id)
    if existing_like:
        raise HTTPException(status_code=400, detail="Blog already liked")
    
    crud.create_like(db=db, user_id=current_user.id, blog_id=blog_id)
    return {"message": "Blog liked successfully"}

# Unlike a blog
@router.delete("/{blog_id}/like")
def unlike_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    crud.delete_like(db=db, user_id=current_user.id, blog_id=blog_id)
    return {"message": "Blog unliked successfully"}



# In routers/blog.py
@router.get("/{blog_id}/media")
def get_blog_media(blog_id: int, db: Session = Depends(get_db)):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if db_blog is None or db_blog.media_content is None:
        raise HTTPException(status_code=404, detail="Media not found")
    
    # Increment view count
    db_blog.views += 1
    db.commit()
    db.refresh(db_blog)
    
    # Return the file with appropriate headers
    return Response(
        content=db_blog.media_content,
        media_type=db_blog.media_type or "application/octet-stream",
        headers={"Content-Disposition": f"inline; filename={db_blog.media_filename}"}
    )