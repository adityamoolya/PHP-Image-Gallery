# routers/search.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel

import schemas
from database import get_db

try:
    from vector_search import vector_search_service
    VECTOR_SEARCH_AVAILABLE = True
except ImportError:
    VECTOR_SEARCH_AVAILABLE = False
    vector_search_service = None

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 10
    threshold: Optional[float] = 0.7

class SearchResult(schemas.Post):
    similarity_score: float

@router.post("/", response_model=List[SearchResult])
async def semantic_search(
    search_query: SearchQuery,
    db: AsyncSession = Depends(get_db)
):
    """
    Perform semantic search on posts using vector embeddings.
    - query: The search text
    - limit: Maximum number of results (default: 10)
    - threshold: Minimum similarity score (default: 0.7)
    """
    if not search_query.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    if not VECTOR_SEARCH_AVAILABLE or not vector_search_service:
        raise HTTPException(
            status_code=503, 
            detail="Vector search not available. Please install required dependencies: pip install numpy sentence-transformers torch"
        )
    
    try:
        similar_posts = await vector_search_service.search_similar_posts(
            db=db,
            query=search_query.query,
            limit=search_query.limit,
            threshold=search_query.threshold
        )
        
        return similar_posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/", response_model=List[SearchResult])
async def semantic_search_get(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    threshold: float = Query(0.7, ge=0.0, le=1.0, description="Minimum similarity score"),
    db: AsyncSession = Depends(get_db)
):
    """
    Perform semantic search on posts using vector embeddings (GET version).
    """
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    if not VECTOR_SEARCH_AVAILABLE or not vector_search_service:
        raise HTTPException(
            status_code=503, 
            detail="Vector search not available. Please install required dependencies: pip install numpy sentence-transformers torch"
        )
    
    try:
        similar_posts = await vector_search_service.search_similar_posts(
            db=db,
            query=q,
            limit=limit,
            threshold=threshold
        )
        
        return similar_posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
