/**
 * Template Loader - Makes all pages use base.html structure
 * 讓所有頁面都能使用 base.html 的結構
 */

// Initialize admin template
function initAdminTemplate(options = {}) {
    const {
        pageTitle = 'Admin Panel',
        activePage = '',
        onReady = null
    } = options;
    
    return new Promise((resolve) => {
        $(document).ready(async function() {
            // Set page title
            document.title = pageTitle + ' - AI-Tracks Studio Admin';
            
            // Load sidebar
            loadAdminSidebar(activePage);
            
            // Load header
            loadAdminHeader(pageTitle);
            
            // Check authentication
            const user = await checkAuth();
            
            if (user) {
                $('#userEmailText').text(user.email);
                
                // Call custom onReady callback
                if (onReady) {
                    onReady(user);
                }
                
                resolve(user);
            }
        });
    });
}

/**
 * Load admin sidebar
 */
function loadAdminSidebar(activePage) {
    const sidebarHTML = `
        <div class="sidebar-header">
            <div class="sidebar-logo">AI-Tracks Studio</div>
            <div class="sidebar-subtitle">後台管理系統</div>
        </div>
        <nav>
            <ul class="sidebar-nav list-unstyled mb-0">
                <li class="nav-section expanded">
                    <div class="nav-section-title">
                        <span><i class="fas fa-boxes me-2"></i> 內容管理</span>
                        <span class="nav-section-icon"><i class="fas fa-chevron-down"></i></span>
                    </div>
                    <ul class="nav-section-items list-unstyled">
                        <li class="nav-item">
                            <a href="/backend/projects" class="nav-link-item ${activePage === 'projects' ? 'active' : ''}">
                                <span class="nav-icon"><i class="fas fa-gamepad"></i></span>
                                <span>Projects 管理</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="/backend/news" class="nav-link-item ${activePage === 'news' ? 'active' : ''}">
                                <span class="nav-icon"><i class="fas fa-newspaper"></i></span>
                                <span>News 管理</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="/backend/about" class="nav-link-item ${activePage === 'about' ? 'active' : ''}">
                                <span class="nav-icon"><i class="fas fa-info-circle"></i></span>
                                <span>About 管理</span>
                            </a>
                        </li>
                    </ul>
                </li>
            </ul>
        </nav>
    `;
    
    $('#adminSidebar').html(sidebarHTML);
    
    // Toggle nav section
    $('.nav-section-title').click(function() {
        $(this).closest('.nav-section').toggleClass('collapsed');
    });
}

/**
 * Load admin header with user dropdown
 */
function loadAdminHeader(pageTitle) {
    const headerHTML = `
        <h1 class="header-title m-0">${pageTitle}</h1>
        <div class="dropdown">
            <button class="btn btn-light d-flex align-items-center gap-1 px-2 py-1 rounded-pill" type="button" id="userDropdown" data-bs-toggle="dropdown">
                <i class="fas fa-user-circle fs-4 text-primary"></i>
                <i class="fas fa-chevron-down small text-muted"></i>
            </button>
            <ul class="dropdown-menu dropdown-menu-end shadow" style="min-width: 200px;">
                <li class="px-3 py-2 border-bottom">
                    <div class="small text-muted">登入身分</div>
                    <div class="fw-bold" id="userEmailText">載入中...</div>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                    <a class="dropdown-item text-danger" href="#" onclick="adminLogout(); return false;">
                        <i class="fas fa-sign-out-alt me-2"></i> 登出
                    </a>
                </li>
            </ul>
        </div>
    `;
    
    $('#adminHeader').html(headerHTML);
    
    // Load current user
    loadCurrentUser();
}

/**
 * Load current user information
 */
async function loadCurrentUser() {
    try {
        const user = await checkAuth();
        if (user) {
            $('#userEmailText').text(user.email);
        }
    } catch (error) {
        console.error('Failed to load user:', error);
    }
}

/**
 * Logout function
 */
async function adminLogout() {
    if (!confirm('確定要登出嗎？')) return;
    
    try {
        await $.ajax({
            url: '/api/admin/logout',
            method: 'POST',
            xhrFields: { withCredentials: true }
        });
        window.location.href = '/backend/login';
    } catch (error) {
        console.error('Logout failed:', error);
        showErrorToast('登出失敗');
    }
}

/**
 * Show Bootstrap loading
 */
function showLoading(containerId) {
    $(`#${containerId}`).html(`
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">載入中...</span>
            </div>
            <p class="mt-3 text-muted">載入中...</p>
        </div>
    `);
}

/**
 * Show error message
 */
function showError(containerId, message) {
    $(`#${containerId}`).html(`
        <div class="alert alert-danger" role="alert">
            <i class="fas fa-exclamation-circle me-2"></i>
            <strong>錯誤：</strong> ${message}
        </div>
    `);
}

/**
 * Show success toast
 */
function showSuccessToast(message) {
    showToast(message, 'success');
}

/**
 * Show error toast
 */
function showErrorToast(message) {
    showToast(message, 'danger');
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    // Create toast container if not exists
    if ($('#toastContainer').length === 0) {
        $('body').append('<div class="toast-container position-fixed top-0 end-0 p-3" id="toastContainer"></div>');
    }
    
    const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas ${icon} me-2"></i> ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const $toast = $(toastHTML);
    $('#toastContainer').append($toast);
    
    const toast = new bootstrap.Toast($toast[0], { delay: 3000 });
    toast.show();
    
    $toast.on('hidden.bs.toast', function() {
        $(this).remove();
    });
}

/**
 * Confirm delete with modal
 */
function confirmDelete(message, onConfirm) {
    const modalHTML = `
        <div class="modal fade" id="confirmModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-danger text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-exclamation-triangle me-2"></i> 確認刪除
                        </h5>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${message}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            <i class="fas fa-times me-1"></i> 取消
                        </button>
                        <button type="button" class="btn btn-danger" id="confirmBtn">
                            <i class="fas fa-trash me-1"></i> 確定刪除
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    $('#confirmModal').remove();
    $('body').append(modalHTML);
    
    const modal = new bootstrap.Modal('#confirmModal');
    modal.show();
    
    $('#confirmBtn').one('click', function() {
        modal.hide();
        if (onConfirm) onConfirm();
    });
    
    $('#confirmModal').on('hidden.bs.modal', function() {
        $(this).remove();
    });
}

/**
 * Format date (using jQuery)
 */
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-TW');
}

/**
 * Format datetime
 */
function formatDateTime(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleString('zh-TW');
}

