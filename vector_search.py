# vector_search.py

try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    VECTOR_SEARCH_AVAILABLE = True
except ImportError:
    VECTOR_SEARCH_AVAILABLE = False
    print("Warning: Vector search dependencies not installed. Install with: pip install numpy sentence-transformers torch")

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
import models

try:
    from config import HUGGINGFACE_API_KEY
except ImportError:
    HUGGINGFACE_API_KEY = None

class VectorSearchService:
    def __init__(self):
        if not VECTOR_SEARCH_AVAILABLE:
            self.model = None
            self.embedding_dimension = 384
            return
        
        try:
            # Initialize the sentence transformer model
            self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            self.embedding_dimension = 384  # Dimension for all-MiniLM-L6-v2
        except Exception as e:
            print(f"Warning: Could not initialize vector search model: {e}")
            self.model = None
            self.embedding_dimension = 384
    
    def generate_embedding(self, text: str) -> list:
        """Generate embedding for the given text"""
        if not text:
            return [0.0] * self.embedding_dimension
        
        if not self.model:
            return [0.0] * self.embedding_dimension
        
        # Clean and prepare text
        clean_text = text.strip()
        if not clean_text:
            return [0.0] * self.embedding_dimension
        
        try:
            # Generate embedding
            embedding = self.model.encode(clean_text)
            return embedding.tolist()
        except Exception as e:
            print(f"Warning: Could not generate embedding: {e}")
            return [0.0] * self.embedding_dimension
    
    def generate_post_embedding(self, post: models.Post) -> list:
        """Generate embedding for a post by combining title, caption, and alt_text"""
        text_parts = []
        
        if post.title:
            text_parts.append(post.title)
        if post.caption:
            text_parts.append(post.caption)
        if post.alt_text:
            text_parts.append(post.alt_text)
        
        # Combine all text parts
        combined_text = " ".join(text_parts)
        return self.generate_embedding(combined_text)
    
    async def search_similar_posts(
        self, 
        db: AsyncSession, 
        query: str, 
        limit: int = 10,
        threshold: float = 0.7
    ) -> list:
        """Search for posts similar to the query using vector similarity"""
        # Generate embedding for the query
        query_embedding = self.generate_embedding(query)
        
        # Convert to numpy array for cosine similarity calculation
        query_vector = np.array(query_embedding)
        
        # Get all posts with embeddings
        result = await db.execute(
            select(models.Post)
            .options(
                models.Post.tags,
                models.Post.album,
                models.Post.author,
                models.Post.comments,
                models.Post.likes
            )
            .filter(models.Post.embedding.isnot(None))
        )
        posts = result.scalars().all()
        
        # Calculate similarities
        similar_posts = []
        if not VECTOR_SEARCH_AVAILABLE or not self.model:
            return similar_posts
            
        for post in posts:
            if post.embedding:
                try:
                    post_vector = np.array(post.embedding)
                    
                    # Calculate cosine similarity
                    similarity = np.dot(query_vector, post_vector) / (
                        np.linalg.norm(query_vector) * np.linalg.norm(post_vector)
                    )
                    
                    if similarity >= threshold:
                        # Add similarity score to post object
                        post.similarity_score = float(similarity)
                        post.likes_count = len(post.likes)
                        similar_posts.append(post)
                except Exception as e:
                    print(f"Warning: Could not calculate similarity for post {post.id}: {e}")
                    continue
        
        # Sort by similarity score (descending)
        similar_posts.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return similar_posts[:limit]

# Global instance
vector_search_service = VectorSearchService()
