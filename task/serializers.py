from rest_framework import serializers
from users.models import CustomUser

from .models import Project, Task, Comment, History, Notification


# =========================
# PROJECT
# =========================

class ProjectSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField()
    tasks_count = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    completion_percent = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    days_remaining = serializers.ReadOnlyField()

    # Аналитика по проекту
    planned_vs_actual_hours = serializers.SerializerMethodField()
    in_progress_tasks_count = serializers.SerializerMethodField()
    new_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'status',
            'manager',
            'manager_name',
            'members',
            'members_count',
            'tasks_count',
            'in_progress_tasks_count',
            'new_tasks_count',
            'planned_hours',
            'actual_hours',
            'planned_vs_actual_hours',
            'completion_percent',
            'is_overdue',
            'days_remaining',
            'start_date',
            'end_date',
            'color',
            'tags',
            'created_at',
            'client',
            'contract_number',
            'budget',
        ]
        read_only_fields = ['actual_hours', 'created_at']

    def get_manager_name(self, obj):
        return str(obj.manager) if obj.manager else '—'

    def get_tasks_count(self, obj):
        return obj.tasks.count()

    def get_in_progress_tasks_count(self, obj):
        return obj.tasks.filter(status='in_progress').count()

    def get_new_tasks_count(self, obj):
        return obj.tasks.filter(status='new').count()

    def get_members_count(self, obj):
        return obj.members.count()

    def get_planned_vs_actual_hours(self, obj):
        return obj.planned_vs_actual_hours


# =========================
# TASK
# =========================

class TaskSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    executor_name = serializers.SerializerMethodField()
    co_executor_names = serializers.SerializerMethodField()
    project_name = serializers.SerializerMethodField()

    is_overdue = serializers.ReadOnlyField()
    completion_days = serializers.ReadOnlyField()
    status_display = serializers.ReadOnlyField()
    priority_display = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'status_display',
            'priority',
            'priority_display',

            'project',
            'project_name',

            'author',
            'author_name',

            'executor',
            'executor_name',

            'co_executors',
            'co_executor_names',

            'deadline',

            'estimated_hours',
            'actual_hours',

            'tags',

            'reopened_count',
            'completed_at',

            'is_overdue',
            'completion_days',

            'created_at'
        ]

        read_only_fields = [
            'author',
            'created_at',
            'completed_at',
            'reopened_count'
        ]

    def get_author_name(self, obj):
        return str(obj.author)

    def get_executor_name(self, obj):
        return str(obj.executor)

    def get_co_executor_names(self, obj):
        return [str(u) for u in obj.co_executors.all()]

    def get_project_name(self, obj):
        return obj.project.name if obj.project else '—'


# =========================
# COMMENT
# =========================

class CommentSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'task',
            'user',
            'user_full_name',
            'text',
            'created_at'
        ]

        read_only_fields = ['user', 'created_at']

    def get_user_full_name(self, obj):

        full_name = f"{obj.user.first_name} {obj.user.last_name} {obj.user.patronymic}".strip()

        # если имя и фамилия пустые
        if not full_name:
            return obj.user.username

        return full_name


# =========================
# HISTORY
# =========================

class HistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = [
            'id',
            'task',
            'changed_by',
            'changed_by_name',
            'old_status',
            'new_status',
            'changed_at'
        ]

    def get_changed_by_name(self, obj):
        return str(obj.changed_by)


# =========================
# NOTIFICATION
# =========================

class NotificationSerializer(serializers.ModelSerializer):
    task_title = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id',
            'type',
            'type_display',
            'message',
            'is_read',
            'task',
            'task_title',
            'created_at'
        ]

    def get_task_title(self, obj):
        return obj.task.title if obj.task else ''

    def get_type_display(self, obj):
        return obj.get_type_display()