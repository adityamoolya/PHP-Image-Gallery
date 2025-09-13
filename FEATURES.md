# ShotPin - Enhanced Features Documentation

## Overview
This document describes the new features added to the ShotPin Pinterest-like application backend.

## New Features Implemented

### 1. Enhanced Likes System ✅
- **Like Count**: All GET endpoints for posts now return `likes_count` field
- **Endpoints Affected**:
  - `GET /api/posts/` - Returns like count for each post
  - `GET /api/posts/{post_id}` - Returns like count for the specific post
- **Implementation**: Automatically calculates and includes like counts in all post responses

### 2. Enhanced Comments System ✅
- **Edit Comments**: New endpoint `PUT /api/comments/{comment_id}` for editing comments
- **User Info**: All comments now returned with complete user information and timestamps
- **Permissions**: Only comment authors or admins can edit/delete comments
- **Endpoints**:
  - `PUT /api/comments/{comment_id}` - Edit a comment
  - `GET /api/comments/post/{post_id}` - Get comments with user info
  - `DELETE /api/comments/{comment_id}` - Delete comment (existing)

### 3. Enhanced Post Deletion ✅
- **Cascade Delete**: When deleting a post, all associated data is automatically removed:
  - All likes for the post
  - All comments on the post
  - Associated images from Cloudinary
- **Implementation**: Enhanced `delete_post` function in CRUD operations

### 4. Vector Search (Semantic Search) ✅
- **Technology**: Uses Hugging Face's `sentence-transformers/all-MiniLM-L6-v2` model
- **Database**: PostgreSQL with pgvector extension for vector storage
- **Auto-embedding**: Posts automatically generate embeddings on creation
- **Endpoints**:
  - `POST /api/search/` - Semantic search with JSON body
  - `GET /api/search/` - Semantic search with query parameters
- **Parameters**:
  - `query`: Search text
  - `limit`: Maximum results (default: 10)
  - `threshold`: Minimum similarity score (default: 0.7)
- **Response**: Returns posts with `similarity_score` field

### 5. AI Image Generation ✅
- **Technology**: Hugging Face Stable Diffusion XL API
- **Storage**: Generated images automatically uploaded to Cloudinary
- **Endpoint**: `POST /api/images/generate/`
- **Request Body**:
  ```json
  {
    "prompt": "A beautiful sunset over mountains"
  }
  ```
- **Response**:
  ```json
  {
    "message": "AI image generated successfully!",
    "url": "https://res.cloudinary.com/...",
    "public_id": "ai-generated/...",
    "prompt": "A beautiful sunset over mountains"
  }
  ```
- **Frontend Form**: Included `ai_image_form.html` for easy integration

### 6. Enhanced Album Management ✅
- **Add Posts**: `POST /api/albums/{album_id}/posts/{post_id}`
- **Remove Posts**: `DELETE /api/albums/{album_id}/posts/{post_id}`
- **Permissions**: Only admins and editors can manage albums
- **Implementation**: Updates post's `album_id` field

## Environment Configuration

### Required Environment Variables
Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/shotpin_db

# Hugging Face API Configuration
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# JWT Configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Setup
1. Install PostgreSQL with pgvector extension
2. Create database: `shotpin_db`
3. Run the application to auto-create tables
4. The `embedding` field will be added to the `posts` table

## New Dependencies Added

```txt
pgvector==0.2.4
sentence-transformers==2.2.2
torch==2.1.0
transformers==4.35.2
requests==2.31.0
numpy==1.24.3
```

## API Endpoints Summary

### New Endpoints
- `POST /api/search/` - Semantic search
- `GET /api/search/` - Semantic search (GET version)
- `POST /api/images/generate/` - AI image generation
- `PUT /api/comments/{comment_id}` - Edit comment
- `POST /api/albums/{album_id}/posts/{post_id}` - Add post to album
- `DELETE /api/albums/{album_id}/posts/{post_id}` - Remove post from album

### Enhanced Endpoints
- `GET /api/posts/` - Now includes `likes_count`
- `GET /api/posts/{post_id}` - Now includes `likes_count`
- `GET /api/comments/post/{post_id}` - Now includes user info
- `DELETE /api/posts/{post_id}` - Now cascades deletes

## Usage Examples

### Semantic Search
```bash
# POST request
curl -X POST "http://localhost:8000/api/search/" \
  -H "Content-Type: application/json" \
  -d '{"query": "beautiful sunset", "limit": 5, "threshold": 0.8}'

# GET request
curl "http://localhost:8000/api/search/?q=beautiful%20sunset&limit=5&threshold=0.8"
```

### AI Image Generation
```bash
curl -X POST "http://localhost:8000/api/images/generate/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"prompt": "A futuristic cityscape at sunset"}'
```

### Edit Comment
```bash
curl -X PUT "http://localhost:8000/api/comments/123" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"content": "Updated comment text"}'
```

### Album Management
```bash
# Add post to album
curl -X POST "http://localhost:8000/api/albums/1/posts/5" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Remove post from album
curl -X DELETE "http://localhost:8000/api/albums/1/posts/5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Frontend Integration

### AI Image Generation Form
The `ai_image_form.html` file provides a complete frontend form for AI image generation. It includes:
- User-friendly interface
- Loading states
- Error handling
- Image display
- Authentication integration

### Search Integration
For semantic search, you can integrate the search endpoints into your frontend search functionality to provide more relevant results based on content similarity rather than just keyword matching.

## Performance Considerations

### Vector Search
- Embeddings are generated once per post creation
- Search is performed in-memory for small datasets
- For production with large datasets, consider using pgvector's built-in similarity functions

### AI Image Generation
- Images are generated asynchronously
- Generated images are cached in Cloudinary
- Consider implementing rate limiting for production use

## Security Notes

- All new endpoints require authentication where appropriate
- AI image generation requires valid user authentication
- Album management restricted to admin/editor roles
- Input validation on all new endpoints

## Future Enhancements

Potential areas for further development:
1. Batch embedding generation for existing posts
2. Image similarity search using visual embeddings
3. Advanced search filters (date, user, album)
4. Caching for frequently searched terms
5. Real-time search suggestions
