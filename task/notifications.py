from .models import Notification
from django.utils import timezone
from datetime import timedelta

def get_user_full_name(user):

    full_name = f"{user.first_name} {user.last_name} {user.patronymic}".strip()

    return full_name if full_name else user.username

def notify_task_assigned(task):
    """При создании/переназначении задачи"""
    # Уведомление исполнителю
    Notification.objects.create(
        user=task.executor,
        task=task,
        type='assigned',
        message=f'📋 Вам назначена задача: «{task.title}»'
    )

    # Уведомление автору, если он не исполнитель
    if task.author_id != task.executor_id:
        Notification.objects.create(
            user=task.author,
            task=task,
            type='assigned',
            message=f'✅ Задача «{task.title}» назначена на {task.executor}'
        )

    # Уведомление соисполнителям
    for co_executor in task.co_executors.all():
        if co_executor.id != task.executor_id and co_executor.id != task.author_id:
            Notification.objects.create(
                user=co_executor,
                task=task,
                type='assigned',
                message=f'👥 Вас добавили соисполнителем в задачу: «{task.title}»'
            )


def notify_status_changed(task, old_status, changed_by):
    """При смене статуса"""
    status_labels = {
        'new': '🟡 Новая',
        'in_progress': '🔵 В процессе',
        'done': '🟢 Завершена'
    }

    message = f'📌 Задача «{task.title}»: {status_labels.get(old_status, old_status)} → {status_labels.get(task.status, task.status)}'

    recipients = set()
    if task.author_id != changed_by.id:
        recipients.add(task.author_id)
    if task.executor_id != changed_by.id:
        recipients.add(task.executor_id)

    # Добавляем соисполнителей
    for co_executor in task.co_executors.all():
        if co_executor.id != changed_by.id:
            recipients.add(co_executor.id)

    for user_id in recipients:
        Notification.objects.create(
            user_id=user_id,
            task=task,
            type='status_changed',
            message=message
        )


def notify_comment_added(comment):
    """При добавлении комментария"""
    task = comment.task
    author_name = get_user_full_name(comment.user)


    message = f'💬 Новый комментарий к задаче «{task.title}» от {author_name}'

    recipients = set()
    recipients.add(task.author_id)
    recipients.add(task.executor_id)

    # Добавляем соисполнителей
    for co_executor in task.co_executors.all():
        recipients.add(co_executor.id)

    recipients.discard(comment.user_id)  # Себе не шлём

    for user_id in recipients:
        Notification.objects.create(
            user_id=user_id,
            task=task,
            type='commented',
            message=message
        )


def notify_overdue_tasks():
    """Проверка просроченных задач и отправка уведомлений (запускать по расписанию)"""
    from .models import Task
    from datetime import datetime

    overdue_tasks = Task.objects.filter(
        deadline__lt=datetime.now(),
        status__in=['new', 'in_progress']
    )

    notifications_created = 0
    for task in overdue_tasks:
        # Проверяем, не отправляли ли уже уведомление сегодня
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        existing = Notification.objects.filter(
            task=task,
            type='overdue',
            created_at__gte=today_start
        ).exists()

        if not existing:
            message = f'⚠️ Задача «{task.title}» просрочена! Срок был: {task.deadline.strftime("%d.%m.%Y %H:%M")}'

            recipients = set()
            recipients.add(task.author_id)
            recipients.add(task.executor_id)
            for co_executor in task.co_executors.all():
                recipients.add(co_executor.id)

            for user_id in recipients:
                Notification.objects.create(
                    user_id=user_id,
                    task=task,
                    type='overdue',
                    message=message
                )
            notifications_created += 1

    return notifications_created


def notify_project_budget_warning(project):
    """Уведомление о перерасходе бюджета проекта"""
    warning = project.budget_overrun_warning
    if warning:
        message = f'💰 Проект «{project.name}»: {warning["message"]}'

        # Уведомляем менеджера проекта
        if project.manager:
            Notification.objects.create(
                user=project.manager,
                task=None,
                type='budget_warning',
                message=message
            )

        # Уведомляем всех участников с ролью manager
        from users.models import CustomUser
        managers = CustomUser.objects.filter(role='manager')
        for manager in managers:
            if manager != project.manager:
                Notification.objects.create(
                    user=manager,
                    task=None,
                    type='budget_warning',
                    message=f'⚠️ {message}'
                )


# ========== НОВАЯ ФУНКЦИЯ: УВЕДОМЛЕНИЕ МЕНЕДЖЕРА О НАЗНАЧЕНИИ НА ПРОЕКТ ==========
def notify_project_manager_assigned(project, manager):
    """Уведомление менеджера о назначении на проект"""
    if not manager:
        return

    message = f'🏢 Вас назначили менеджером проекта "{project.name}"'

    Notification.objects.create(
        user=manager,
        task=None,
        type='project_assigned',
        message=message
    )

    # Дополнительное уведомление автору (кто назначил)
    # Не отправляем, так как автор и так знает


def notify_project_created(project, created_by):
    """Уведомление о создании проекта (для администратора/менеджера)"""
    message = f'✅ Создан новый проект "{project.name}"'

    Notification.objects.create(
        user=created_by,
        task=None,
        type='project_created',
        message=message
    )


def get_unread_notifications_count(user):
    """Получить количество непрочитанных уведомлений"""
    return Notification.objects.filter(user=user, is_read=False).count()


def mark_all_notifications_read(user):
    """Отметить все уведомления как прочитанные"""
    return Notification.objects.filter(user=user, is_read=False).update(is_read=True)


def get_notifications_for_user(user, limit=50):
    """Получить уведомления пользователя с дополнительной информацией"""
    notifications = Notification.objects.filter(user=user)[:limit]

    result = []
    for notif in notifications:
        result.append({
            'id': notif.id,
            'type': notif.get_type_display(),
            'type_key': notif.type,
            'message': notif.message,
            'is_read': notif.is_read,
            'created_at': notif.created_at.isoformat(),
            'created_at_formatted': notif.created_at.strftime('%d.%m.%Y %H:%M'),
            'task_id': notif.task.id if notif.task else None,
            'task_title': notif.task.title if notif.task else None,
        })

    return result