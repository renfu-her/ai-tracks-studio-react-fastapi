// Admin Panel Common JavaScript
// Version: 2024120401

// Skip if already loaded (but still define functions below)
if (window.ADMIN_JS_LOADED) {
    console.log('[admin.js] Already loaded v2024120401');
} else {
    window.ADMIN_JS_LOADED = true;
    console.log('[admin.js] Loading v2024120401');
}

// API Base URL
window.API_BASE = window.API_BASE || '';

// Check authentication
window.checkAuth = async function checkAuth() {
    console.log('[checkAuth] Starting authentication check...');
    try {
        const response = await fetch('/api/admin/me', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Accept': 'application/json'
            }
        });
        
        console.log('[checkAuth] Response status:', response.status, response.statusText);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('[checkAuth] API error:', response.status, errorText);
            
            if (response.status === 401 || response.status === 403) {
                console.log('[checkAuth] Unauthorized, redirecting to login');
                window.location.href = '/backend/login';
                return null;
            }
            
            // For other errors, return null but don't redirect
            return null;
        }
        
        const user = await response.json();
        console.log('[checkAuth] User profile loaded successfully:', user);
        
        // Validate user data
        if (!user || typeof user !== 'object') {
            console.error('[checkAuth] Invalid user data:', user);
            return null;
        }
        
        return user;
    } catch (error) {
        console.error('[checkAuth] Exception occurred:', error);
        console.error('[checkAuth] Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        });
        
        // Only redirect on network errors
        if (error.name === 'TypeError' && (error.message.includes('fetch') || error.message.includes('Failed to fetch'))) {
            console.error('[checkAuth] Network error detected, redirecting to login');
            window.location.href = '/backend/login';
        }
        
        return null;
    }
};

// Logout function
window.logout = async function logout() {
    if (!confirm('確定要登出嗎？')) return;
    
    try {
        await fetch('/api/admin/logout', {
            method: 'POST',
            credentials: 'include'
        });
        window.location.href = '/backend/login';
    } catch (error) {
        console.error('Logout failed:', error);
        alert('登出失敗');
    }
};

// API fetch wrapper
window.apiRequest = async function apiRequest(url, options = {}) {
    const defaultOptions = {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const response = await fetch(url, { ...defaultOptions, ...options });
    
    if (response.status === 401) {
        alert('請重新登入');
        window.location.href = '/backend/login';
        throw new Error('Unauthorized');
    }
    
    if (response.status === 204) {
        return null;
    }
    
    const data = await response.json();
    
    if (!response.ok) {
        throw new Error(data.detail || 'Request failed');
    }
    
    return data;
};

// Upload image (returns only filename)
// Make sure it's in global scope
window.uploadImage = async function uploadImage(file) {
    console.log('[uploadImage] Uploading file:', file.name, file.size, 'bytes');
    
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/api/admin/upload/image', {
        method: 'POST',
        credentials: 'include',
        body: formData
    });
    
    console.log('Upload response status:', response.status);
    
    if (!response.ok) {
        const error = await response.json();
        console.error('Upload failed:', error);
        throw new Error(error.detail || '上傳失敗');
    }
    
    const result = await response.json();
    console.log('[uploadImage] Upload success:', result);
    return result.filename; // Only return filename
};

// Verify function is defined
console.log('[admin.js] uploadImage defined:', typeof window.uploadImage);

// Get full image URL from filename
// Make sure it's in global scope
window.getImageUrl = function getImageUrl(filename) {
    if (!filename) {
        console.log('[getImageUrl] empty filename');
        return '';
    }
    if (filename.startsWith('http://') || filename.startsWith('https://')) {
        console.log('getImageUrl: external URL:', filename);
        return filename;
    }
    if (filename.startsWith('/backend/static/uploads/')) {
        console.log('getImageUrl: already has path:', filename);
        return filename;
    }
    const url = `/backend/static/uploads/${filename}`;
    console.log('[getImageUrl] generated URL:', url);
    return url;
};

// Verify function is defined
console.log('[admin.js] getImageUrl defined:', typeof window.getImageUrl);

// Show loading
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>載入中...</p>
            </div>
        `;
    }
}

// Show error
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #e53e3e;">
                <p style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">錯誤</p>
                <p>${message}</p>
            </div>
        `;
    }
}

// Format datetime
window.formatDateTime = function formatDateTime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('zh-TW');
};

// Format date
window.formatDate = function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-TW');
};

console.log('[admin.js] All functions loaded successfully');
console.log('[admin.js] Functions available:', {
    checkAuth: typeof window.checkAuth,
    logout: typeof window.logout,
    apiRequest: typeof window.apiRequest,
    uploadImage: typeof window.uploadImage,
    getImageUrl: typeof window.getImageUrl
});
