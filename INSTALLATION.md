# ShotPin Installation Guide

## Quick Start

### 1. Install Basic Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the backend directory with:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/shotpin_db
SECRET_KEY=your-secret-key-here
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 3. Run the Application
```bash
python run.py
```

The API will be available at: http://localhost:8000
Documentation: http://localhost:8000/docs

## Optional Features

### Vector Search (Semantic Search)
To enable semantic search functionality:
```bash
pip install numpy sentence-transformers torch
```

### AI Image Generation
To enable AI image generation:
```bash
pip install requests
```

And add to your `.env` file:
```env
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

## Database Setup

### PostgreSQL with pgvector
1. Install PostgreSQL
2. Install pgvector extension:
   ```sql
   CREATE EXTENSION vector;
   ```
3. Create your database:
   ```sql
   CREATE DATABASE shotpin_db;
   ```

## Troubleshooting

### "main app not found" Error
This usually means there are missing dependencies. The application now handles missing optional dependencies gracefully:

- **Vector Search**: If numpy/sentence-transformers are missing, search endpoints will return 503 errors
- **AI Image Generation**: If requests is missing, image generation will return 503 errors
- **Core Features**: All basic features (posts, comments, likes, albums) work without additional dependencies

### Missing Dependencies
The application will show warnings for missing optional dependencies but will still start. Install them as needed:

```bash
# For vector search
pip install numpy sentence-transformers torch

# For AI image generation  
pip install requests

# For environment variables
pip install python-dotenv
```

## Features Available

### ✅ Always Available (Core Features)
- Posts CRUD operations
- Comments with edit functionality
- Likes with count
- Albums with post management
- Image upload to Cloudinary
- Authentication

### 🔧 Optional Features (Require Additional Setup)
- **Vector Search**: Semantic search using embeddings
- **AI Image Generation**: Generate images from text prompts

## API Endpoints

### Core Endpoints
- `GET /api/posts/` - List posts with like counts
- `POST /api/posts/` - Create post
- `GET /api/posts/{id}` - Get post with like count
- `PUT /api/posts/{id}` - Update post
- `DELETE /api/posts/{id}` - Delete post (cascades)

- `GET /api/comments/post/{id}` - Get comments with user info
- `POST /api/comments/` - Create comment
- `PUT /api/comments/{id}` - Edit comment
- `DELETE /api/comments/{id}` - Delete comment

- `POST /api/posts/{id}/like` - Like post
- `DELETE /api/posts/{id}/like` - Unlike post

- `GET /api/albums/` - List albums
- `POST /api/albums/` - Create album
- `POST /api/albums/{id}/posts/{post_id}` - Add post to album
- `DELETE /api/albums/{id}/posts/{post_id}` - Remove post from album

### Optional Endpoints
- `POST /api/search/` - Semantic search (requires vector search)
- `GET /api/search/` - Semantic search (requires vector search)
- `POST /api/images/generate/` - AI image generation (requires AI service)

## Development

### Running in Development Mode
```bash
python run.py
```

### Running with Uvicorn Directly
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API
Visit http://localhost:8000/docs for interactive API documentation.
