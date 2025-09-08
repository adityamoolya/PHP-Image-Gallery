from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import schemas, crud
from database import get_db
from auth_utils import get_current_active_user

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

# Get comments for a blog
@router.get("/blog/{blog_id}", response_model=List[schemas.Comment])
def get_comments_for_blog(blog_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_by_blog(db, blog_id=blog_id)

# Create comment
@router.post("/", response_model=schemas.Comment)
def create_comment(
    comment: schemas.CommentCreate,
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    db_blog = crud.get_blog(db, blog_id=blog_id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return crud.create_comment(db=db, comment_data=comment, author_id=current_user.id, blog_id=blog_id)

# Delete comment
@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check if user is comment author or admin
    if db_comment.author_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    crud.delete_comment(db=db, comment_id=comment_id)
    return {"message": "Comment deleted successfully"}  