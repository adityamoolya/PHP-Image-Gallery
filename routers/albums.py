# routers/albums.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import schemas, crud
from database import get_db
from auth_utils import get_current_active_user

router = APIRouter(
    prefix="/albums",
    tags=["Albums"]
)

@router.post("/", response_model=schemas.Album)
async def create_new_album(
    album: schemas.AlbumCreate, 
    db: AsyncSession = Depends(get_db), 
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Creates a new album.
    - Requires authentication.
    - User must have the 'admin' or 'editor' role.
    """
    # --- ADDED: Role-based permission check ---
    if current_user.role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create an album."
        )

    # Check if an album with this name already exists
    db_album = await crud.get_album_by_name(db, name=album.name)
    if db_album:
        raise HTTPException(status_code=400, detail="Album with this name already exists.")
    
    return await crud.create_album(db=db, album=album)

@router.get("/", response_model=List[schemas.Album])
async def read_all_albums(db: AsyncSession = Depends(get_db)):
    """
    Retrieves a list of all albums.
    - No authentication required.
    """
    albums = await crud.get_albums(db)
    return albums

@router.post("/{album_id}/posts/{post_id}")
async def add_post_to_album(
    album_id: int,
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Adds a post to an album.
    - Requires authentication.
    - User must have 'admin' or 'editor' role.
    """
    if current_user.role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify albums."
        )
    
    # Check if album exists
    db_album = await crud.get_album_by_id(db, album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Check if post exists
    db_post = await crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Add post to album
    await crud.add_post_to_album(db=db, album_id=album_id, post_id=post_id)
    return {"message": "Post added to album successfully"}

@router.delete("/{album_id}/posts/{post_id}")
async def remove_post_from_album(
    album_id: int,
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user)
):
    """
    Removes a post from an album.
    - Requires authentication.
    - User must have 'admin' or 'editor' role.
    """
    if current_user.role not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify albums."
        )
    
    # Check if album exists
    db_album = await crud.get_album_by_id(db, album_id=album_id)
    if not db_album:
        raise HTTPException(status_code=404, detail="Album not found")
    
    # Check if post exists
    db_post = await crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Remove post from album
    await crud.remove_post_from_album(db=db, album_id=album_id, post_id=post_id)
    return {"message": "Post removed from album successfully"}