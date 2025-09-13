# 📸 PHP-IMAGE-GALLERY

A **full-stack Image Gallery project** that allows users to **upload, manage, and explore images**.  
The project is built with a **Frontend (PHP)** and a **Backend (FastAPI + PostgreSQL)**, deployed on **Railway**.  

We are also planning to implement **Vector Search 🔍** and **AI Image Generation 🎨** in future updates.  

---

## 🚀 Live Links

- 🌐 **Frontend App (PHP):** [Live Demo](https://php-image-gallery-production.up.railway.app/)  
- 📖 **Backend API (FastAPI + Docs):** [API Docs](https://dependable-manifestation-production-2bc6.up.railway.app/docs)  

---

## 📂 Project Structure

```bash
.
├── backend/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── album.py
│   │   ├── auth.py
│   │   ├── comments.py
│   │   ├── images.py
│   │   ├── post.py
│   ├── auth_utils.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── requirements.txt
│   ├── runtime.txt
│   ├── Procfile
│
├── frontend_final/        # Frontend (PHP-based)
│
├── public/                # Static assets
├── src/
│   ├── api/               # API integration
│   ├── styles/            # CSS styles
│   ├── App.js             # React/JS entry file
│   ├── main.css
│   ├── index.html
│
├── server.js              # Frontend server config
├── package.json
├── package-lock.json
├── runtime.txt
├── Procfile
├── .gitignore
└── README.md


##✨ Features

✅ User Authentication – Signup / Login to manage your account
✅ Image Uploading – Upload your images to the gallery
✅ Image Management – View, delete, and manage images easily
✅ Category Support – Organize images into categories
✅ Tags System – Tag images for easy filtering
✅ Deployed Backend – Accessible with FastAPI Swagger docs
✅ Deployed Frontend – Live and working with backend integration

##🔮 Upcoming Features
🔍 Vector Search – Search images by similarity using embeddings
🎨 AI Image Generation – Generate new images using Hugging Face API
💬 Comments & Likes – Add interactivity to image posts
🗑️ Delete & Edit Support – Manage uploaded content fully

⚡ Tech Stack
Frontend:

PHP

HTML, CSS, JavaScript

Backend:

Python (FastAPI)

SQLAlchemy ORM

PostgreSQL (Hosted on Railway)

Planned AI Integration:

Hugging Face Inference API → Image Generation

FAISS / Pinecone / Weaviate → Vector Search

Deployment:

Railway (Backend + Frontend)

📡 API Endpoints
🔑 Authentication
POST /auth/signup → Register a new user

POST /auth/login → Login user & get token

🖼️ Images
GET /images/ → List all images

POST /images/upload → Upload new image

DELETE /images/{id} → Delete image by ID

📝 Posts
GET /posts/posts → Get all posts

POST /posts/create → Create new post

GET /posts/{id} → Get post by ID

DELETE /posts/{id} → Delete post

📂 Categories
GET /categories/ → List all categories

🏷️ Tags
GET /tags/ → List all tags

💬 Comments
GET /comments/{post_id} → List comments for a post

POST /comments/add → Add a comment
