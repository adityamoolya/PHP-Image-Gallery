from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "viewer"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Tag Schemas
class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Comment Schemas
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    author: User
    blog_id: int
    created_at: datetime
    is_approved: bool

    class Config:
        from_attributes = True

# Blog Schemas
class BlogBase(BaseModel):
    title: str
    content: str
    content_type: str = "text"
    content_format: str = "text"
    published: bool = True
    category_id: Optional[int] = None
    media_content: Optional[str] = None  # Base64 encoded file content
    media_filename: Optional[str] = None
    media_type: Optional[str] = None

class BlogCreate(BlogBase):
    tags: List[str] = []

class Blog(BlogBase):
    id: int
    author: User
    category: Optional[Category] = None
    tags: List[Tag] = []
    comments: List[Comment] = []
    views: int
    likes_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    media_path: Optional[str] = None

    class Config:
        from_attributes = True

# Like Schema
class Like(BaseModel):
    id: int
    user: User
    blog_id: int

    class Config:
        from_attributes = True