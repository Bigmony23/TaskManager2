from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH + DASHBOARD
    path('', views.index),
    path('login/', views.login_view),
    path('dashboard/', views.dashboard),
    path('logout/', views.logout_view),

    # TASKS
    path('task/create/', views.task_create),
    path('task/edit/<int:task_id>/', views.task_edit),
    path('task/delete/<int:task_id>/', views.task_delete),
    path('task/change-status/<int:task_id>/', views.change_status),

    # PROJECTS
    path('projects/', views.projects_list, name='projects'),
    path('projects/create/', views.project_create),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='projects_edit'),
    # ========== ДОБАВИТЬ ЭТУ СТРОКУ ==========
    path('projects/<int:project_id>/analytics/', views.project_analytics, name='project_analytics'),

    # API
    path('api/', include('api.urls')),
]