##PHP-IMAGE- GALLERY


A full-stack **Image Gallery** project that allows users to upload, manage, and explore images.  
The project is built with a **Frontend (PHP)** and a **Backend (FastAPI)** deployed on **Railway**.  
We are also planning to implement **Vector Search 🔍** and **AI Image Generation 🎨** in future updates.

---

## 🚀 Live Links

- **Frontend App (PHP)**: [🌐 Live Demo](https://php-image-gallery-production.up.railway.app/)  
- **Backend API (FastAPI + Docs)**: [📖 API Docs](https://dependable-manifestation-production-2bc6.up.railway.app/docs-backend)

---

## 📂 Project Structure"

.
├── backend/
│ ├── routers/
│ │ ├── pycache/
│ │ ├── init.py
│ │ ├── album.py
│ │ ├── auth.py
│ │ ├── comments.py
│ │ ├── images.py
│ │ ├── post.py
│ ├── Procfile
│ ├── auth_utils.py
│ ├── crud.py
│ ├── database.py
│ ├── main.py
│ ├── models.py
│ ├── requirements.txt
│ ├── runtime.txt
│ ├── schemas.py
│
├── frontend_final/
│
├── node_modules/
│
├── public/
│
├── src/
│ ├── api/
│ ├── styles/
│ ├── App.js
│ ├── main.css
│ ├── index.html
│
├── Procfile
├── README.md
├── package-lock.json
├── package.json
├── runtime.txt
├── server.js
├── .gitignore


---

## ✨ Features

✅ **User Authentication** – Signup / Login to manage your account  
✅ **Image Uploading** – Upload your images to the gallery  
✅ **Image Management** – View, delete, and manage images easily  
✅ **Category Support** – Organize images into categories  
✅ **Tags System** – Tag images for easy filtering  
✅ **Deployed Backend** – Accessible with FastAPI Swagger docs  
✅ **Deployed Frontend** – Live and working with backend integration  

---

## 🔮 Upcoming Features

🔍 **Vector Search** – Search images by similarity using embeddings  
🎨 **AI Image Generation** – Generate new images using Hugging Face API  
💬 **Comments & Likes** – Add interactivity to image posts  
🗑️ **Delete & Edit Support** – Manage uploaded content fully  

---

## ⚡ Tech Stack

**Frontend:**  
- PHP  
- HTML, CSS, JavaScript  

**Backend:**  
- Python (FastAPI)  
- SQLAlchemy + Database (PostgreSQL on Railway)  

**Planned AI Integration:**  
- Hugging Face Inference API for Image Generation  
- FAISS / Pinecone / Weaviate for Vector Search  

**Deployment:**  
- Railway (Backend + Frontend)   

---

