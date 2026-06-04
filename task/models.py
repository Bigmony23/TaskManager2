from django.db import models
from django.utils import timezone
from datetime import date
from django.db.models import Sum, Count, Q

from users.models import CustomUser
from django.utils import timezone

# =========================
# PROJECT
# =========================

class Project(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активный'),
        ('on_hold', 'Приостановлен'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    # В class Project добавить:


    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_projects'
    )

    members = models.ManyToManyField(
        CustomUser,
        related_name='projects',
        blank=True
    )

    # сроки
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # плановые часы (для оценки загруженности)
    planned_hours = models.FloatField(default=0)
    actual_hours = models.FloatField(default=0)

    # визуал
    color = models.CharField(max_length=7, default='#667eea')
    tags = models.CharField(max_length=500, blank=True)
    client = models.CharField(max_length=200, blank=True)
    contract_number = models.CharField(max_length=100, blank=True)
    budget = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    # =========================
    # ПРОГРЕСС ПРОЕКТА
    # =========================

    @property
    def tasks_count(self):
        return self.tasks.count()

    @property
    def completed_tasks_count(self):
        return self.tasks.filter(status='done').count()

    @property
    def in_progress_tasks_count(self):
        return self.tasks.filter(status='in_progress').count()

    @property
    def new_tasks_count(self):
        return self.tasks.filter(status='new').count()

    @property
    def completion_percent(self):
        total = self.tasks.count()
        if total == 0:
            return 0
        return round(self.completed_tasks_count / total * 100, 1)

    @property
    def is_overdue(self):
        return self.end_date and self.end_date < date.today() and self.status != 'completed'

    @property
    def days_remaining(self):
        if not self.end_date:
            return None
        delta = self.end_date - date.today()
        return max(delta.days, 0)

    # =========================
    # ЗАГРУЖЕННОСТЬ И ЭФФЕКТИВНОСТЬ
    # =========================

    def update_actual_hours(self):
        """Обновить фактические часы из задач"""
        total = self.tasks.aggregate(total=Sum('actual_hours'))['total'] or 0
        self.actual_hours = total
        self.save(update_fields=['actual_hours'])

    @property
    def planned_vs_actual_hours(self):
        """Сравнение плановых и фактических часов"""
        if self.planned_hours == 0:
            return {'planned': 0, 'actual': self.actual_hours, 'diff': self.actual_hours, 'percent': 0}
        percent = round(self.actual_hours / self.planned_hours * 100, 1)
        return {
            'planned': self.planned_hours,
            'actual': self.actual_hours,
            'diff': self.actual_hours - self.planned_hours,
            'percent': percent
        }

    def get_forecast(self):
        """Прогноз завершения проекта"""
        from datetime import timedelta

        # Задачи завершённые за последние 7 дней
        completed_last_week = self.tasks.filter(
            status='done',
            completed_at__gte=timezone.now() - timedelta(days=7)
        ).count()

        remaining = self.tasks.filter(status__in=['new', 'in_progress']).count()

        if completed_last_week == 0 or remaining == 0:
            return None

        days_needed = round(remaining / (completed_last_week / 7))
        forecast_date = timezone.now().date() + timedelta(days=days_needed)

        return {
            'days_needed': days_needed,
            'estimated_date': forecast_date.isoformat(),
            'speed_per_week': completed_last_week,
            'remaining_tasks': remaining,
        }

    def get_burndown_data(self):
        """Данные для burndown chart"""
        from datetime import timedelta

        if not self.start_date or not self.end_date:
            return []

        days_range = (self.end_date - self.start_date).days
        if days_range <= 0:
            return []

        # Ограничиваем количество точек для больших проектов (максимум 60)
        step = max(1, days_range // 60)

        data = []
        for i in range(0, days_range + 1, step):
            current_date = self.start_date + timedelta(days=i)
            tasks_until = self.tasks.filter(created_at__date__lte=current_date)
            remaining = tasks_until.filter(status__in=['new', 'in_progress']).count()
            data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'remaining': remaining,
            })

        return data
    def get_executor_stats(self):
        """Статистика по всем исполнителям проекта"""
        from django.db.models import Count, Q

        executors = CustomUser.objects.filter(
            Q(assigned_tasks__project=self) | Q(co_assigned_tasks__project=self)
        ).distinct()

        stats = []
        for executor in executors:
            main_tasks = self.tasks.filter(executor=executor)
            co_tasks = self.tasks.filter(co_executors=executor)
            all_tasks = (main_tasks | co_tasks).distinct()

            total = all_tasks.count()
            if total == 0:
                continue

            completed = all_tasks.filter(status='done').count()
            in_progress = all_tasks.filter(status='in_progress').count()
            new_tasks = all_tasks.filter(status='new').count()
            overdue = all_tasks.filter(
                deadline__lt=timezone.now(),
                status__in=['new', 'in_progress']
            ).count()
            completion_rate = round(completed / total * 100, 1)

            completed_tasks = all_tasks.filter(status='done', completed_at__isnull=False)
            avg_days = 0
            if completed_tasks.exists():
                total_days = sum([
                    (t.completed_at - t.created_at).total_seconds() / 86400
                    for t in completed_tasks if t.completed_at
                ])
                avg_days = round(total_days / completed_tasks.count(), 1)

            active_count = all_tasks.filter(status__in=['new', 'in_progress']).count()

            # Эффективность: 60% за выполнение, 40% за отсутствие просрочек
            efficiency = 0
            if total > 0:
                completion_score = (completed / total) * 60
                overdue_score = (1 - (overdue / total)) * 40
                efficiency = round(completion_score + overdue_score, 1)

            stats.append({
                'executor_id': executor.id,
                'executor_name': str(executor),
                'total': total,
                'completed': completed,
                'in_progress': in_progress,
                'new_tasks': new_tasks,
                'overdue': overdue,
                'overdue_rate': round(overdue / total * 100, 1) if total > 0 else 0,
                'completion_rate': completion_rate,
                'avg_completion_days': avg_days,
                'active_count': active_count,
                'efficiency': efficiency,  # ← поле efficiency
            })

        return sorted(stats, key=lambda x: x['efficiency'], reverse=True)

    def get_project_progress(self):
        """Общий прогресс проекта"""
        total = self.tasks_count
        if total == 0:
            return {
                'total': 0,
                'completed': 0,
                'in_progress': 0,
                'new': 0,
                'completion_percent': 0,
                'overdue_tasks': 0
            }

        overdue = self.tasks.filter(
            deadline__lt=timezone.now(),
            status__in=['new', 'in_progress']
        ).count()

        return {
            'total': total,
            'completed': self.completed_tasks_count,
            'in_progress': self.in_progress_tasks_count,
            'new': self.new_tasks_count,
            'completion_percent': self.completion_percent,
            'overdue_tasks': overdue
        }


# =========================
# TASK
# =========================

class Task(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('done', 'Завершена'),
    )

    PRIORITY_CHOICES = (
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий'),
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)

    deadline = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )

    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='assigned_tasks'
    )

    co_executors = models.ManyToManyField(
        CustomUser,
        related_name='co_assigned_tasks',
        blank=True
    )

    # время
    estimated_hours = models.FloatField(null=True, blank=True)
    actual_hours = models.FloatField(null=True, blank=True)

    # доп
    tags = models.CharField(max_length=200, blank=True)

    # контроль
    reopened_count = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    # =========================
    # СТАТУС И ПРОГРЕСС ЗАДАЧИ
    # =========================

    @property
    def is_overdue(self):
        return self.deadline and self.deadline < timezone.now() and self.status != 'done'

    @property
    def completion_days(self):
        if self.completed_at and self.created_at:
            delta = self.completed_at - self.created_at
            return round(delta.total_seconds() / 86400, 1)
        return None

    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    @property
    def priority_display(self):
        return dict(self.PRIORITY_CHOICES).get(self.priority, self.priority)

    def save(self, *args, **kwargs):
        if self.status == 'done' and not self.completed_at:
            self.completed_at = timezone.now()

        if self.pk:
            old = Task.objects.filter(pk=self.pk).first()
            if old and old.status == 'done' and self.status != 'done':
                self.reopened_count += 1

        super().save(*args, **kwargs)

    # =========================
    # ИНФОРМАЦИЯ ОБ ИСПОЛНИТЕЛЯХ
    # =========================

    def get_all_executors(self):
        """Все исполнители задачи (основной + соисполнители)"""
        executors = [self.executor]
        executors.extend(self.co_executors.all())
        return executors

    @property
    def executors_count(self):
        """Количество исполнителей"""
        return 1 + self.co_executors.count()


# =========================
# COMMENT
# =========================

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -> {self.task.title}'


# =========================
# HISTORY
# =========================

class History(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='history')
    changed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    old_status = models.CharField(max_length=20, null=True, blank=True)
    new_status = models.CharField(max_length=20)

    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.task.title}: {self.old_status} → {self.new_status}'


# =========================
# NOTIFICATION
# =========================

class Notification(models.Model):
    TYPE_CHOICES = (
        ('assigned', 'Назначена задача'),
        ('status_changed', 'Изменён статус'),
        ('commented', 'Комментарий'),
        ('overdue', 'Просрочена'),
        ('budget_warning', 'Предупреждение о бюджете'),
        ('project_assigned', 'Назначен менеджером проекта'),  # НОВЫЙ ТИП
        ('project_created', 'Создан новый проект'),  # НОВЫЙ ТИП
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True
    )

    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.get_type_display()}] {self.message[:40]}'


# =========================
# СИГНАЛЫ
# =========================

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=Task)
@receiver(post_delete, sender=Task)
def update_project_actual_hours(sender, instance, **kwargs):
    try:
        if instance.project_id and instance.project:
            instance.project.update_actual_hours()
    except Project.DoesNotExist:
        pass


@receiver(post_save, sender=Task)
def add_executor_to_project_members(sender, instance, **kwargs):
    """Автоматически добавляем исполнителя в участники проекта"""
    if instance.project and instance.executor:
        instance.project.members.add(instance.executor)
        for co in instance.co_executors.all():
            instance.project.members.add(co)