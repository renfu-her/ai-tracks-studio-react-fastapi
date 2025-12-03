// Admin Panel Common JavaScript

// API Base URL
const API_BASE = '';

// Check authentication
async function checkAuth() {
    try {
        const response = await fetch('/api/admin/me', {
            credentials: 'include'
        });
        
        if (!response.ok) {
            window.location.href = '/backend/login';
            return null;
        }
        
        const user = await response.json();
        return user;
    } catch (error) {
        console.error('Auth check failed:', error);
        window.location.href = '/backend/login';
        return null;
    }
}

// Logout function
async function logout() {
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
}

// API fetch wrapper
async function apiRequest(url, options = {}) {
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
}

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

// Format date
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-TW');
}

// Format datetime
function formatDateTime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('zh-TW');
}

