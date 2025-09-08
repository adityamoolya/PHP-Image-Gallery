from sqlalchemy import Column, Integer, LargeBinary, String, Boolean, DateTime, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Association table for many-to-many relationship between blogs and tags
blog_tags = Table(
    'blog_tags', Base.metadata,
    Column('blog_id', Integer, ForeignKey('blogs.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(20), default="viewer")  # admin, editor, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    blogs = relationship("Blog", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    likes = relationship("Like", back_populates="user")

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    content_type = Column(String(20), default="text")  # text, photo, quote, link, video, audio, uploader
    content_format = Column(String(20), default="text")  # text, markdown, raw
    media_path = Column(String(500), nullable=True)
    published = Column(Boolean, default=True)
    views = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    author_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Relationships
    author = relationship("User", back_populates="blogs")
    category = relationship("Category", back_populates="blogs")
    comments = relationship("Comment", back_populates="blog")
    tags = relationship("Tag", secondary=blog_tags, back_populates="blogs")
    likes = relationship("Like", back_populates="blog")


    media_content = Column(LargeBinary, nullable=True)  # For storing file content directly
    media_filename = Column(String(255), nullable=True)  # Original filename
    media_type = Column(String(50), nullable=True) 

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    blogs = relationship("Blog", back_populates="category")

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    blogs = relationship("Blog", secondary=blog_tags, back_populates="tags")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_approved = Column(Boolean, default=True)
    
    # Foreign keys
    author_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    # Relationships
    author = relationship("User", back_populates="comments")
    blog = relationship("Blog", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id])

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    
    # Relationships
    user = relationship("User", back_populates="likes")
    blog = relationship("Blog", back_populates="likes")