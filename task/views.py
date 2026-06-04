from django.utils import timezone
from django.db.models import Q
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from users.models import CustomUser
from .models import Task, Project, Comment, History, Notification
from .serializers import TaskSerializer, ProjectSerializer, CommentSerializer, NotificationSerializer
from .permissions import CanEditTask
from .notifications import (
    notify_task_assigned,
    notify_status_changed,
    notify_comment_added
)

from rest_framework.exceptions import PermissionDenied
# =========================
# TASK VIEWSET
# =========================
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, CanEditTask]

    def get_permissions(self):


        if self.action == 'comments':
            return [IsAuthenticated()]

        return [permission() for permission in self.permission_classes]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'executor', 'project']
    search_fields = ['title', 'description']
    ordering_fields = ['deadline', 'created_at', 'priority']

    def get_queryset(self):
        user = self.request.user

        if user.role in ['admin', 'manager']:
            return Task.objects.all().select_related('project', 'executor', 'author').prefetch_related('co_executors')

        return Task.objects.filter(
            Q(executor=user) | Q(co_executors=user)
        ).distinct().select_related('project', 'executor', 'author').prefetch_related('co_executors')

    def perform_create(self, serializer):
        task = serializer.save(author=self.request.user)
        notify_task_assigned(task)

    def destroy(self, request, *args, **kwargs):
        """Удаление задачи с проверкой прав"""
        instance = self.get_object()
        user = request.user

        # Admin может удалять всё
        if user.role == 'admin':
            project = instance.project
            result = super().destroy(request, *args, **kwargs)
            if project:
                project.update_actual_hours()
            return result

        # Manager может удалять только свои задачи
        if user.role == 'manager' and instance.author == user:
            project = instance.project
            result = super().destroy(request, *args, **kwargs)
            if project:
                project.update_actual_hours()
            return result

        # Employee не может удалять

        raise PermissionDenied('У вас нет прав на удаление этой задачи')

    def perform_update(self, serializer):
        old_task = self.get_object()
        old_status = old_task.status

        task = serializer.save()

        if old_status != task.status:
            History.objects.create(
                task=task,
                changed_by=self.request.user,
                old_status=old_status,
                new_status=task.status
            )
            notify_status_changed(task, old_status, self.request.user)

    # =========================
    # COMMENTS
    # =========================
    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):

        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {'error': 'Задача не найдена'},
                status=404
            )

        user = request.user

        # Проверка доступа
        if user.role == 'employee':

            allowed = (
                    task.executor == user or
                    user in task.co_executors.all()
            )

            if not allowed:
                return Response(
                    {'error': 'Нет доступа'},
                    status=403
                )

        if request.method == 'GET':
            return Response(
                CommentSerializer(
                    task.comments.all(),
                    many=True
                ).data
            )

        text = request.data.get('text')

        if not text:
            return Response(
                {'error': 'Текст комментария обязателен'},
                status=400
            )

        comment = Comment.objects.create(
            task=task,
            user=request.user,
            text=text
        )

        notify_comment_added(comment)

        return Response(
            CommentSerializer(comment).data,
            status=201
        )

    # =========================
    # CO-EXECUTORS
    # =========================
    @action(detail=True, methods=['post'])
    def add_co_executor(self, request, pk=None):
        task = self.get_object()
        user_id = request.data.get('user_id')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        task.co_executors.add(user)
        if task.project:
            task.project.members.add(user)
        return Response({'status': 'added'})

    @action(detail=True, methods=['post'])
    def remove_co_executor(self, request, pk=None):
        task = self.get_object()
        task.co_executors.remove(request.data.get('user_id'))
        return Response({'status': 'removed'})

    # =========================
    # MY TASKS
    # =========================
    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        user = request.user

        tasks = Task.objects.filter(
            Q(executor=user) | Q(co_executors=user)
        ).distinct()

        return Response(TaskSerializer(tasks, many=True).data)

    # =========================
    # АНАЛИТИКА ПО ЗАДАЧАМ (ОБЩАЯ)
    # =========================
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        user = request.user
        if user.role == 'employee':
            return Response({'error': 'Доступ запрещён'}, status=403)

        tasks = Task.objects.all()

        # Статистика по статусам
        status_stats = {
            'new': tasks.filter(status='new').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'done': tasks.filter(status='done').count(),
            'overdue': tasks.filter(
                deadline__lt=timezone.now(),
                status__in=['new', 'in_progress']
            ).count()
        }

        # Статистика по приоритетам
        priority_stats = {
            'low': tasks.filter(priority=1).count(),
            'medium': tasks.filter(priority=2).count(),
            'high': tasks.filter(priority=3).count()
        }

        # Статистика по исполнителям (загруженность)
        executor_stats = []
        for executor in CustomUser.objects.filter(role='employee'):
            user_tasks = tasks.filter(Q(executor=executor) | Q(co_executors=executor)).distinct()
            total = user_tasks.count()
            if total == 0:
                continue

            completed = user_tasks.filter(status='done').count()
            in_progress = user_tasks.filter(status='in_progress').count()
            overdue = user_tasks.filter(
                deadline__lt=timezone.now(),
                status__in=['new', 'in_progress']
            ).count()

            # Эффективность
            efficiency = 0
            if total > 0:
                completion_score = (completed / total) * 60
                overdue_score = (1 - overdue / total) * 40 if total > 0 else 40
                efficiency = round(completion_score + overdue_score, 1)

            executor_stats.append({
                'id': executor.id,
                'name': str(executor),
                'total': total,
                'completed': completed,
                'in_progress': in_progress,
                'overdue': overdue,
                'completion_rate': round(completed / total * 100, 1),
                'efficiency': efficiency
            })

        return Response({
            'status_stats': status_stats,
            'priority_stats': priority_stats,
            'executor_stats': sorted(executor_stats, key=lambda x: x['efficiency'], reverse=True)
        })


# =========================
# PROJECT VIEWSET
# =========================
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role in ['admin', 'manager']:
            return Project.objects.all()

        return Project.objects.filter(members=user)



    def perform_create(self, serializer):
        project = serializer.save()
        project.members.add(self.request.user)
        if self.request.user.role == 'manager':
            project.manager = self.request.user
            project.save()

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise PermissionDenied('Только администратор может удалять проекты')
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        project = self.get_object()
        return Response(TaskSerializer(project.tasks.all(), many=True).data)

    @action(detail=True, methods=['get'])
    def analytics(self, request, pk=None):
        """Аналитика по проекту - загруженность исполнителей и прогресс"""
        project = self.get_object()
        tasks = project.tasks.all()

        # Прогресс проекта
        progress = {
            'total': tasks.count(),
            'completed': tasks.filter(status='done').count(),
            'in_progress': tasks.filter(status='in_progress').count(),
            'new': tasks.filter(status='new').count(),
            'completion_percent': project.completion_percent,
            'overdue_tasks': tasks.filter(
                deadline__lt=timezone.now(),
                status__in=['new', 'in_progress']
            ).count()
        }

        # Статистика по исполнителям
        executor_stats = project.get_executor_stats()

        # Прогноз завершения
        forecast = project.get_forecast()

        # Burndown данные
        burndown_data = project.get_burndown_data()

        return Response({
            'project_id': project.id,
            'project_name': project.name,
            'progress': progress,
            'executor_stats': executor_stats,
            'completion_percent': project.completion_percent,
            'planned_hours': project.planned_hours,
            'actual_hours': project.actual_hours,
            'planned_vs_actual_hours': project.planned_vs_actual_hours,
            'days_remaining': project.days_remaining,
            'is_overdue': project.is_overdue,
            'forecast': forecast,
            'burndown_data': burndown_data,
        })

# =========================
# NOTIFICATIONS
# =========================
class NotificationViewSet(viewsets.GenericViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=False)
    def list_all(self, request):
        return Response(self.serializer_class(self.get_queryset()[:50], many=True).data)

    @action(detail=False)
    def unread_count(self, request):
        qs = self.get_queryset()
        return Response({
            "count": qs.filter(is_read=False).count(),
            "items": self.serializer_class(qs.filter(is_read=False)[:10], many=True).data
        })

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notif = self.get_queryset().filter(pk=pk).first()
        if notif:
            notif.is_read = True
            notif.save()
        return Response({"status": "ok"})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({"status": "ok"})