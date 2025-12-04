/**
 * Common UI Components for Admin Panel
 * Uses jQuery and Bootstrap 5
 */

$(document).ready(function() {
    // Load common components
    loadSidebar();
    loadHeader();
});

/**
 * Load sidebar navigation
 */
function loadSidebar() {
    const currentPath = window.location.pathname;
    
    const sidebarHTML = `
        <div class="sidebar-header">
            <div class="sidebar-logo">AI-Tracks Studio</div>
            <div class="sidebar-subtitle">後台管理系統</div>
        </div>
        <nav>
            <ul class="sidebar-nav list-unstyled">
                <li class="nav-section expanded">
                    <div class="nav-section-title">
                        <span><i class="fas fa-boxes me-2"></i> 內容管理</span>
                        <span class="nav-section-icon"><i class="fas fa-chevron-down"></i></span>
                    </div>
                    <ul class="nav-section-items list-unstyled">
                        <li class="nav-item">
                            <a href="/backend/projects" class="nav-link-item ${currentPath.includes('/projects') ? 'active' : ''}">
                                <span class="nav-icon"><i class="fas fa-gamepad"></i></span>
                                <span>Projects 管理</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="/backend/news" class="nav-link-item ${currentPath.includes('/news') ? 'active' : ''}">
                                <span class="nav-icon"><i class="fas fa-newspaper"></i></span>
                                <span>News 管理</span>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="/backend/about" class="nav-link-item ${currentPath.includes('/about') ? 'active' : ''}">
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
 * Load header with user info
 */
function loadHeader() {
    const headerHTML = `
        <h1 class="header-title" id="dynamicHeaderTitle">Loading...</h1>
        <div class="header-actions">
            <span class="user-info" id="currentUserEmail">
                <i class="fas fa-user-circle me-2"></i>
                <span id="userEmailText">載入中...</span>
            </span>
            <button onclick="adminLogout()" class="btn btn-danger btn-sm">
                <i class="fas fa-sign-out-alt me-1"></i> 登出
            </button>
        </div>
    `;
    
    $('#adminHeader').html(headerHTML);
    
    // Load user info
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
        alert('登出失敗');
    }
}

/**
 * Set page title
 */
function setPageTitle(title) {
    $('#pageTitle').text(title + ' - AI-Tracks Studio Admin');
    $('#dynamicHeaderTitle').text(title);
}

/**
 * Show loading spinner (Bootstrap 5)
 */
function showBootstrapLoading(containerId) {
    $(`#${containerId}`).html(`
        <div class="spinner-container">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">載入中...</span>
            </div>
            <p class="mt-3 text-muted">載入中...</p>
        </div>
    `);
}

/**
 * Show error message (Bootstrap 5)
 */
function showBootstrapError(containerId, message) {
    $(`#${containerId}`).html(`
        <div class="alert alert-danger" role="alert">
            <i class="fas fa-exclamation-circle me-2"></i>
            <strong>錯誤：</strong> ${message}
        </div>
    `);
}

/**
 * Show success toast (Bootstrap 5)
 */
function showSuccessToast(message) {
    // Create toast container if not exists
    if ($('#toastContainer').length === 0) {
        $('body').append(`
            <div class="toast-container position-fixed top-0 end-0 p-3" id="toastContainer"></div>
        `);
    }
    
    const toastHTML = `
        <div class="toast align-items-center text-white bg-success border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-check-circle me-2"></i> ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const $toast = $(toastHTML);
    $('#toastContainer').append($toast);
    
    const toast = new bootstrap.Toast($toast[0]);
    toast.show();
    
    // Remove after hide
    $toast.on('hidden.bs.toast', function() {
        $(this).remove();
    });
}

/**
 * Show error toast (Bootstrap 5)
 */
function showErrorToast(message) {
    if ($('#toastContainer').length === 0) {
        $('body').append(`
            <div class="toast-container position-fixed top-0 end-0 p-3" id="toastContainer"></div>
        `);
    }
    
    const toastHTML = `
        <div class="toast align-items-center text-white bg-danger border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-exclamation-circle me-2"></i> ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    const $toast = $(toastHTML);
    $('#toastContainer').append($toast);
    
    const toast = new bootstrap.Toast($toast[0]);
    toast.show();
    
    $toast.on('hidden.bs.toast', function() {
        $(this).remove();
    });
}

/**
 * Confirm delete with Bootstrap modal
 */
function confirmDelete(message, onConfirm) {
    const modalHTML = `
        <div class="modal fade" id="confirmDeleteModal" tabindex="-1">
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
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                        <button type="button" class="btn btn-danger" id="confirmDeleteBtn">
                            <i class="fas fa-trash me-1"></i> 確定刪除
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    $('#confirmDeleteModal').remove();
    
    // Append and show
    $('body').append(modalHTML);
    const modal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    modal.show();
    
    // Handle confirm
    $('#confirmDeleteBtn').one('click', function() {
        modal.hide();
        onConfirm();
    });
    
    // Clean up after hide
    $('#confirmDeleteModal').on('hidden.bs.modal', function() {
        $(this).remove();
    });
}

