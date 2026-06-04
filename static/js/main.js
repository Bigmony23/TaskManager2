// ========== Глобальные переменные ==========
let accessToken = localStorage.getItem('access_token');
let refreshToken = localStorage.getItem('refresh_token');
let userRole = localStorage.getItem('user_role');

// ========== Уведомления ==========
let notificationInterval = null;

// ========== Навигация ==========
function updateNavigation() {
    const navButtons = document.getElementById('nav-buttons');
    if (navButtons && accessToken) {
        navButtons.innerHTML = `
            <div class="dropdown">
                <button class="btn btn-outline-light dropdown-toggle" data-bs-toggle="dropdown">
                    <i class="fas fa-user"></i> Профиль
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a href="/projects/" class="dropdown-item"><i class="fas fa-folder"></i> Проекты</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><button class="dropdown-item" onclick="toggleTheme()"><i class="fas fa-moon"></i> Тёмная тема</button></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><button class="dropdown-item text-danger" onclick="logout()"><i class="fas fa-sign-out-alt"></i> Выход</button></li>
                </ul>
            </div>
            <div class="notification-bell" onclick="toggleNotifications()">
                <i class="fas fa-bell"></i>
                <span id="notification-badge" class="badge bg-danger" style="display: none; position: absolute; top: -5px; right: -10px; font-size: 10px;">0</span>
            </div>
        `;
    }
}

// ========== Уведомления ==========
async function pollNotifications() {
    const token = getToken();
    if (!token) return;

    try {
        const response = await fetch('/api/notifications/unread_count/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const data = await response.json();
            const badge = document.getElementById('notification-badge');
            if (badge) {
                if (data.count > 0) {
                    badge.textContent = data.count > 99 ? '99+' : data.count;
                    badge.style.display = 'inline-block';
                } else {
                    badge.style.display = 'none';
                }
            }
        }
    } catch (error) {
        console.error('Ошибка загрузки уведомлений:', error);
    }
}

function toggleNotifications() {
    const token = getToken();
    if (!token) return;

    // Создаём или открываем модальное окно с уведомлениями
    let modal = document.getElementById('notificationsModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'notificationsModal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"><i class="fas fa-bell"></i> Уведомления</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body" id="notifications-list">
                        <div class="text-center py-4"><i class="fas fa-spinner fa-spin"></i> Загрузка...</div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-sm btn-outline-primary" onclick="markAllNotificationsRead()">Все прочитаны</button>
                        <button type="button" class="btn btn-sm btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    // Загружаем уведомления
    fetch('/api/notifications/list_all/', {
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(res => res.json())
    .then(data => {
        const container = document.getElementById('notifications-list');
        if (data.length === 0) {
            container.innerHTML = '<div class="text-center py-4 text-muted"><i class="fas fa-bell-slash fa-2x mb-2"></i><p>Нет уведомлений</p></div>';
        } else {
            container.innerHTML = data.map(n => `
                <div class="notification-item ${n.is_read ? 'read' : 'unread'}" data-id="${n.id}">
                    <div class="notification-icon">
                        <i class="fas fa-${n.type === 'assigned' ? 'tasks' : n.type === 'status_changed' ? 'exchange-alt' : n.type === 'commented' ? 'comment' : 'clock'}"></i>
                    </div>
                    <div class="notification-content">
                        <div class="notification-message">${escapeHtml(n.message)}</div>
                        <div class="notification-date">${new Date(n.created_at).toLocaleString()}</div>
                    </div>
                    ${!n.is_read ? `<button class="notification-read" onclick="markNotificationRead(${n.id})"><i class="fas fa-check"></i></button>` : ''}
                </div>
            `).join('');
        }
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    })
    .catch(error => console.error('Ошибка:', error));
}

async function markNotificationRead(notificationId) {
    const token = getToken();
    await fetch(`/api/notifications/${notificationId}/mark_read/`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    pollNotifications();
    toggleNotifications();
}

async function markAllNotificationsRead() {
    const token = getToken();
    await fetch('/api/notifications/mark_all_read/', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    pollNotifications();
    toggleNotifications();
}

// ========== Вход ==========
document.getElementById('login-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/token/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            accessToken = data.access;
            refreshToken = data.refresh;

            // Получаем роль пользователя
            const userResponse = await fetch('/api/users/me/', {
                headers: { 'Authorization': `Bearer ${data.access}` }
            });
            if (userResponse.ok) {
                const userData = await userResponse.json();
                localStorage.setItem('user_role', userData.role);
                userRole = userData.role;
            }

            window.location.href = '/dashboard/';
        } else {
            alert('Неверный логин или пароль');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка соединения');
    }
});

// ========== Выход ==========
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_role');
    window.location.href = '/';
}

// ========== Токены ==========
function getToken() {
    return localStorage.getItem('access_token');
}

async function refreshAccessToken() {
    const refresh = localStorage.getItem('refresh_token');
    if (!refresh) return false;

    try {
        const response = await fetch('/api/token/refresh/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refresh })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            accessToken = data.access;
            return true;
        }

        logout();
        return false;
    } catch (error) {
        console.error('Ошибка обновления токена:', error);
        return false;
    }
}

// ========== Тёмная тема ==========
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
}

function loadTheme() {
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-theme');
    }
}

// ========== Вспомогательные функции ==========
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ========== Загрузка информации о пользователе ==========
async function loadUserInfo() {
    const token = getToken();
    if (token) {
        try {
            const response = await fetch('/api/users/me/', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                const user = await response.json();
                const userNameElement = document.getElementById('userName');
                const userRoleElement = document.getElementById('userRole');
                const userAvatarElement = document.getElementById('userAvatar');

                if (userNameElement) userNameElement.textContent = user.username;
                if (userRoleElement) {
                    const roleMap = { 'admin': 'Администратор', 'manager': 'Менеджер', 'employee': 'Исполнитель' };
                    userRoleElement.textContent = roleMap[user.role] || user.role;
                }
                if (userAvatarElement) {
                    userAvatarElement.textContent = user.username.charAt(0).toUpperCase();
                }
                if (user.role) localStorage.setItem('user_role', user.role);
            }
        } catch(e) {
            console.error('Ошибка загрузки пользователя:', e);
        }
    }
}

// ========== Инициализация ==========
document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
    loadUserInfo();
    updateNavigation();

    // Запускаем опрос уведомлений
    if (getToken()) {
        pollNotifications();
        setInterval(pollNotifications, 30000);
    }
});

// ========== Стили для уведомлений ==========
const notificationStyles = `
<style>
.notification-bell {
    position: relative;
    cursor: pointer;
    margin-left: 15px;
    font-size: 1.2rem;
    color: white;
}
.notification-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    border-bottom: 1px solid var(--border-color);
    transition: background 0.2s;
}
.notification-item:hover {
    background: rgba(102, 126, 234, 0.05);
}
.notification-item.unread {
    background: rgba(102, 126, 234, 0.1);
}
.notification-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
}
.notification-content {
    flex: 1;
}
.notification-message {
    font-size: 0.9rem;
    color: var(--text-primary);
}
.notification-date {
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 4px;
}
.notification-read {
    background: none;
    border: none;
    color: #10b981;
    cursor: pointer;
    padding: 5px;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', notificationStyles);