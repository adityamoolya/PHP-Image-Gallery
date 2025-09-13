// API Configuration
const API_BASE_URL = 'https://dependable-manifestation-production-2bc6.up.railway.app';

// State Management
let currentPosts = [];
let currentAlbums = [];
let currentPage = 0;
let isLoading = false;
let currentFilter = 'all';
let currentSearch = '';
let currentUser = null;
let authToken = null;

// DOM Elements
const postsGrid = document.getElementById('postsGrid');
const loadingSpinner = document.getElementById('loadingSpinner');
const emptyState = document.getElementById('emptyState');
const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const loadMoreBtn = document.getElementById('loadMoreBtn');
const filterTags = document.getElementById('filterTags');
const postModal = document.getElementById('postModal');
const modalClose = document.getElementById('modalClose');

// Auth Elements
const authButtons = document.getElementById('authButtons');
const userMenu = document.getElementById('userMenu');
const userInfo = document.getElementById('userInfo');
const loginBtn = document.getElementById('loginBtn');
const registerBtn = document.getElementById('registerBtn');
const logoutBtn = document.getElementById('logoutBtn');
const loginModal = document.getElementById('loginModal');
const registerModal = document.getElementById('registerModal');
const loginModalClose = document.getElementById('loginModalClose');
const registerModalClose = document.getElementById('registerModalClose');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const showRegister = document.getElementById('showRegister');
const showLogin = document.getElementById('showLogin');

// Post Creation Elements
const createPostBtn = document.getElementById('createPostBtn');
const createPostModal = document.getElementById('createPostModal');
const createPostModalClose = document.getElementById('createPostModalClose');
const createPostForm = document.getElementById('createPostForm');
const cancelPost = document.getElementById('cancelPost');
const postImage = document.getElementById('postImage');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');

// Albums Elements
const manageAlbumsBtn = document.getElementById('manageAlbumsBtn');
const albumsModal = document.getElementById('albumsModal');
const albumsModalClose = document.getElementById('albumsModalClose');
const albumsList = document.getElementById('albumsList');
const createAlbumBtn = document.getElementById('createAlbumBtn');
const createAlbumModal = document.getElementById('createAlbumModal');
const createAlbumModalClose = document.getElementById('createAlbumModalClose');
const createAlbumForm = document.getElementById('createAlbumForm');
const cancelAlbum = document.getElementById('cancelAlbum');

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    // Check if user is already logged in
    checkAuthStatus();
    await loadPosts();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    // Search functionality
    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });

    // Load more posts
    loadMoreBtn.addEventListener('click', loadMorePosts);

    // Modal functionality
    modalClose.addEventListener('click', closeModal);
    postModal.addEventListener('click', (e) => {
        if (e.target === postModal) {
            closeModal();
        }
    });

    // Navigation filters
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (!e.target.classList.contains('dropdown-btn')) {
                handleFilterChange(e.target.dataset.filter);
            }
        });
    });

    // Share functionality
    document.getElementById('shareBtn').addEventListener('click', sharePost);

    // Auth functionality
    loginBtn.addEventListener('click', () => openAuthModal('login'));
    registerBtn.addEventListener('click', () => openAuthModal('register'));
    logoutBtn.addEventListener('click', logout);
    
    loginModalClose.addEventListener('click', () => closeAuthModal('login'));
    registerModalClose.addEventListener('click', () => closeAuthModal('register'));
    
    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);
    
    showRegister.addEventListener('click', (e) => {
        e.preventDefault();
        closeAuthModal('login');
        openAuthModal('register');
    });
    
    showLogin.addEventListener('click', (e) => {
        e.preventDefault();
        closeAuthModal('register');
        openAuthModal('login');
    });
    
    // Setup post and album listeners
    setupPostAndAlbumListeners();
}

// API Functions
async function fetchPosts(params = {}) {
    try {
        const queryParams = new URLSearchParams({
            skip: params.skip || 0,
            limit: params.limit || 10,
            ...params
        });

        // Use the correct API endpoint with double posts path
        const response = await fetch(`${API_BASE_URL}/api/posts/posts/?${queryParams}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching posts:', error);
        showError('Failed to load posts. Please try again.');
        return [];
    }
}

// Albums require authentication, so we'll skip this for now
async function fetchAlbums() {
    // Albums require authentication, not available without login
    return [];
}

// Data Loading Functions
async function loadPosts(reset = false) {
    if (isLoading) return;
    
    isLoading = true;
    showLoading(true);

    if (reset) {
        currentPage = 0;
        currentPosts = [];
    }

    const params = {
        skip: currentPage * 10,
        limit: 10
    };

    if (currentFilter !== 'all' && currentFilter !== 'search') {
        params.album = currentFilter;
    }

    if (currentSearch) {
        params.search = currentSearch;
    }

    try {
        const posts = await fetchPosts(params);
        
        if (reset) {
            currentPosts = posts;
        } else {
            currentPosts = [...currentPosts, ...posts];
        }

        currentPage++;
        renderPosts();
        
        // Show/hide load more button
        loadMoreBtn.style.display = posts.length === 10 ? 'block' : 'none';
        
        // Show empty state if no posts
        if (currentPosts.length === 0) {
            showEmptyState(true);
        } else {
            showEmptyState(false);
        }
    } catch (error) {
        console.error('Error loading posts:', error);
    } finally {
        isLoading = false;
        showLoading(false);
    }
}

async function loadAlbums() {
    try {
        currentAlbums = await fetchAlbums();
        renderAlbumDropdown();
    } catch (error) {
        console.error('Error loading albums:', error);
    }
}

async function loadMorePosts() {
    await loadPosts(false);
}

// Rendering Functions
function renderPosts() {
    postsGrid.innerHTML = '';
    
    currentPosts.forEach(post => {
        const postElement = createPostElement(post);
        postsGrid.appendChild(postElement);
    });
}

function createPostElement(post) {
    const postDiv = document.createElement('div');
    postDiv.className = 'post-card';
    postDiv.innerHTML = `
        <div class="post-image">
            <img src="${post.image_url}" alt="${post.alt_text || post.title}" loading="lazy">
            <div class="post-overlay">
                <div class="post-actions">
                    <button class="action-btn view-btn" onclick="openModal(${post.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn like-btn" onclick="toggleLike(${post.id})">
                        <i class="fas fa-heart"></i>
                        <span>${post.likes_count || 0}</span>
                    </button>
                </div>
            </div>
        </div>
        <div class="post-info">
            <h3 class="post-title">${post.title}</h3>
            <div class="post-meta">
                <span class="post-author">
                    <i class="fas fa-user"></i>
                    ${post.author.username}
                </span>
                <span class="post-date">
                    <i class="fas fa-calendar"></i>
                    ${formatDate(post.created_at)}
                </span>
            </div>
            <div class="post-tags">
                ${post.tags.map(tag => `<span class="tag">${tag.name}</span>`).join('')}
            </div>
        </div>
    `;
    
    return postDiv;
}

function renderAlbumDropdown() {
    albumDropdown.innerHTML = '';
    
    currentAlbums.forEach(album => {
        const albumItem = document.createElement('div');
        albumItem.className = 'dropdown-item';
        albumItem.innerHTML = `
            <button class="album-btn" data-album="${album.name}">
                ${album.name}
            </button>
        `;
        
        albumItem.addEventListener('click', () => {
            handleFilterChange(album.name);
        });
        
        albumDropdown.appendChild(albumItem);
    });
}

// Event Handlers
function handleSearch() {
    currentSearch = searchInput.value.trim();
    currentFilter = currentSearch ? 'search' : 'all';
    loadPosts(true);
}

function handleFilterChange(filter) {
    currentFilter = filter;
    currentSearch = '';
    searchInput.value = '';
    
    // Update active nav button
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    if (filter === 'all') {
        document.querySelector('[data-filter="all"]').classList.add('active');
    }
    
    loadPosts(true);
}

// Modal Functions
function openModal(postId) {
    const post = currentPosts.find(p => p.id === postId);
    if (!post) return;

    // Populate modal content
    document.getElementById('modalImage').src = post.image_url;
    document.getElementById('modalImage').alt = post.alt_text || post.title;
    document.getElementById('modalTitle').textContent = post.title;
    document.getElementById('modalAuthor').textContent = post.author.username;
    document.getElementById('modalDate').textContent = formatDate(post.created_at);
    document.getElementById('modalViews').textContent = post.views;
    document.getElementById('modalCaption').textContent = post.caption || '';
    document.getElementById('likeCount').textContent = post.likes_count || 0;

    // Render tags
    const modalTags = document.getElementById('modalTags');
    modalTags.innerHTML = post.tags.map(tag => 
        `<span class="tag">${tag.name}</span>`
    ).join('');

    postModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    postModal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

function toggleLike(postId) {
    // This would require authentication in a real app
    console.log('Like functionality requires authentication');
    showNotification('Please log in to like posts', 'info');
}

function sharePost() {
    if (navigator.share) {
        navigator.share({
            title: document.getElementById('modalTitle').textContent,
            text: document.getElementById('modalCaption').textContent,
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => {
            showNotification('Link copied to clipboard!', 'success');
        });
    }
}

// Utility Functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function showLoading(show) {
    loadingSpinner.style.display = show ? 'flex' : 'none';
}

function showEmptyState(show) {
    emptyState.style.display = show ? 'flex' : 'none';
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;

    // Add to page
    document.body.appendChild(notification);

    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    // Remove notification
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (postModal.style.display === 'flex') {
            closeModal();
        } else if (loginModal.style.display === 'flex') {
            closeAuthModal('login');
        } else if (registerModal.style.display === 'flex') {
            closeAuthModal('register');
        }
    }
});

// Authentication Functions
function checkAuthStatus() {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('currentUser');
    
    if (token && user) {
        authToken = token;
        currentUser = JSON.parse(user);
        updateAuthUI();
    }
}

function updateAuthUI() {
    if (currentUser) {
        authButtons.style.display = 'none';
        userMenu.style.display = 'flex';
        userInfo.textContent = `Welcome, ${currentUser.username}`;
    } else {
        authButtons.style.display = 'flex';
        userMenu.style.display = 'none';
    }
}

async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                password: password
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            
            // Get user info
            const userResponse = await fetch(`${API_BASE_URL}/api/auth/users/me/`, {
                headers: {
                    'Authorization': `Bearer ${authToken}`
                }
            });
            
            if (userResponse.ok) {
                currentUser = await userResponse.json();
                
                // Store in localStorage
                localStorage.setItem('authToken', authToken);
                localStorage.setItem('currentUser', JSON.stringify(currentUser));
                
                updateAuthUI();
                closeAuthModal('login');
                showNotification('Login successful!', 'success');
                
                // Clear form
                loginForm.reset();
            }
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Login failed. Please try again.', 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });
        
        if (response.ok) {
            showNotification('Registration successful! Please login.', 'success');
            closeAuthModal('register');
            openAuthModal('login');
            registerForm.reset();
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Registration failed', 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showNotification('Registration failed. Please try again.', 'error');
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    updateAuthUI();
    showNotification('Logged out successfully', 'success');
}

function openAuthModal(type) {
    if (type === 'login') {
        loginModal.style.display = 'flex';
    } else if (type === 'register') {
        registerModal.style.display = 'flex';
    }
    document.body.style.overflow = 'hidden';
}

function closeAuthModal(type) {
    if (type === 'login') {
        loginModal.style.display = 'none';
    } else if (type === 'register') {
        registerModal.style.display = 'none';
    }
    document.body.style.overflow = 'auto';
}

// Post Creation Functions
async function handleCreatePost(e) {
    e.preventDefault();
    
    if (!authToken) {
        showNotification('Please login to create posts', 'error');
        return;
    }
    
    const formData = new FormData();
    const imageFile = postImage.files[0];
    
    if (!imageFile) {
        showNotification('Please select an image', 'error');
        return;
    }
    
    try {
        // First upload the image
        const uploadFormData = new FormData();
        uploadFormData.append('file', imageFile);
        
        const uploadResponse = await fetch(`${API_BASE_URL}/api/images/images/upload/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            body: uploadFormData
        });
        
        if (!uploadResponse.ok) {
            throw new Error('Image upload failed');
        }
        
        const uploadData = await uploadResponse.json();
        
        // Then create the post
        const postData = {
            title: document.getElementById('postTitle').value,
            caption: document.getElementById('postCaption').value,
            alt_text: document.getElementById('postAltText').value,
            license: document.getElementById('postLicense').value,
            privacy: document.getElementById('postPrivacy').value,
            album_id: document.getElementById('postAlbum').value ? parseInt(document.getElementById('postAlbum').value) : null,
            tags: document.getElementById('postTags').value.split(',').map(tag => tag.trim()).filter(tag => tag),
            image_url: uploadData.url,
            image_public_id: uploadData.public_id
        };
        
        const postResponse = await fetch(`${API_BASE_URL}/api/posts/posts/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(postData)
        });
        
        if (postResponse.ok) {
            showNotification('Post created successfully!', 'success');
            closeModal('createPost');
            createPostForm.reset();
            imagePreview.style.display = 'none';
            await loadPosts(true); // Reload posts
        } else {
            const error = await postResponse.json();
            showNotification(error.detail || 'Failed to create post', 'error');
        }
    } catch (error) {
        console.error('Create post error:', error);
        showNotification('Failed to create post. Please try again.', 'error');
    }
}

function handleImagePreview(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

// Albums Functions
async function loadAlbums() {
    if (!authToken) return [];
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/albums/albums/`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            return await response.json();
        }
        return [];
    } catch (error) {
        console.error('Error loading albums:', error);
        return [];
    }
}

async function handleCreateAlbum(e) {
    e.preventDefault();
    
    if (!authToken) {
        showNotification('Please login to create albums', 'error');
        return;
    }
    
    const albumData = {
        name: document.getElementById('albumName').value,
        description: document.getElementById('albumDescription').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/albums/albums/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(albumData)
        });
        
        if (response.ok) {
            showNotification('Album created successfully!', 'success');
            closeModal('createAlbum');
            createAlbumForm.reset();
            await loadAlbumsList(); // Reload albums
            await loadAlbumsForPost(); // Update post form albums
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Failed to create album', 'error');
        }
    } catch (error) {
        console.error('Create album error:', error);
        showNotification('Failed to create album. Please try again.', 'error');
    }
}

async function loadAlbumsList() {
    const albums = await loadAlbums();
    albumsList.innerHTML = '';
    
    albums.forEach(album => {
        const albumCard = document.createElement('div');
        albumCard.className = 'album-card';
        albumCard.innerHTML = `
            <h3>${album.name}</h3>
            <p>${album.description || 'No description'}</p>
            <div class="album-actions">
                <button class="btn-edit" onclick="editAlbum(${album.id})">Edit</button>
                <button class="btn-delete" onclick="deleteAlbum(${album.id})">Delete</button>
            </div>
        `;
        albumsList.appendChild(albumCard);
    });
}

async function loadAlbumsForPost() {
    const albums = await loadAlbums();
    const albumSelect = document.getElementById('postAlbum');
    albumSelect.innerHTML = '<option value="">No Album</option>';
    
    albums.forEach(album => {
        const option = document.createElement('option');
        option.value = album.id;
        option.textContent = album.name;
        albumSelect.appendChild(option);
    });
}

// Modal Functions
function openModal(type) {
    if (type === 'createPost') {
        createPostModal.style.display = 'flex';
        loadAlbumsForPost(); // Load albums for the form
    } else if (type === 'albums') {
        albumsModal.style.display = 'flex';
        loadAlbumsList(); // Load albums list
    } else if (type === 'createAlbum') {
        createAlbumModal.style.display = 'flex';
    }
    document.body.style.overflow = 'hidden';
}

function closeModal(type) {
    if (type === 'createPost') {
        createPostModal.style.display = 'none';
    } else if (type === 'albums') {
        albumsModal.style.display = 'none';
    } else if (type === 'createAlbum') {
        createAlbumModal.style.display = 'none';
    }
    document.body.style.overflow = 'auto';
}

// Add event listeners for new functionality
function setupPostAndAlbumListeners() {
    // Post Creation functionality
    createPostBtn.addEventListener('click', () => openModal('createPost'));
    createPostModalClose.addEventListener('click', () => closeModal('createPost'));
    cancelPost.addEventListener('click', () => closeModal('createPost'));
    createPostForm.addEventListener('submit', handleCreatePost);
    postImage.addEventListener('change', handleImagePreview);

    // Albums functionality
    manageAlbumsBtn.addEventListener('click', () => openModal('albums'));
    albumsModalClose.addEventListener('click', () => closeModal('albums'));
    createAlbumBtn.addEventListener('click', () => openModal('createAlbum'));
    createAlbumModalClose.addEventListener('click', () => closeModal('createAlbum'));
    cancelAlbum.addEventListener('click', () => closeModal('createAlbum'));
    createAlbumForm.addEventListener('submit', handleCreateAlbum);
}

