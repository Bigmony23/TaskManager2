from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from datetime import datetime

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.shortcuts import redirect
from users.models import CustomUser
from task.models import Task, Project, History
from task.notifications import (
    notify_task_assigned,
    notify_status_changed
)


# ===================== AUTH =====================

def index(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)

            refresh = RefreshToken.for_user(user)

            request.session['jwt_access'] = str(refresh.access_token)
            request.session['jwt_refresh'] = str(refresh)

            messages.success(request, f'Добро пожаловать, {user.username}')
            return redirect('/dashboard/')

        messages.error(request, 'Неверный логин или пароль')
        return redirect('/')

    return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/login')  # или '/'

# ===================== DASHBOARD =====================

# ===================== DASHBOARD =====================

@login_required
def dashboard(request):
    user = request.user

    if user.role == 'admin':
        tasks = Task.objects.all()
    elif user.role == 'manager':
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(Q(executor=user) | Q(co_executors=user)).distinct()

    # Статистика по задачам
    total = tasks.count()
    completed = tasks.filter(status='done').count()
    in_progress = tasks.filter(status='in_progress').count()
    new_count = tasks.filter(status='new').count()
    overdue = tasks.filter(
        deadline__lt=datetime.now(),
        status__in=['new', 'in_progress']
    ).count()

    # Статистика по приоритетам
    priority_low = tasks.filter(priority=1).count()
    priority_medium = tasks.filter(priority=2).count()
    priority_high = tasks.filter(priority=3).count()

    # Статистика по исполнителям (загруженность)
    executor_stats = []
    if user.role in ['admin', 'manager']:
        for executor in CustomUser.objects.filter(role='employee'):
            user_tasks = tasks.filter(Q(executor=executor) | Q(co_executors=executor)).distinct()
            total_user = user_tasks.count()
            if total_user == 0:
                continue

            completed_user = user_tasks.filter(status='done').count()
            in_progress_user = user_tasks.filter(status='in_progress').count()
            overdue_user = user_tasks.filter(
                deadline__lt=datetime.now(),
                status__in=['new', 'in_progress']
            ).count()

            efficiency = 0
            if total_user > 0:
                completion_score = (completed_user / total_user) * 60
                overdue_score = (1 - overdue_user / total_user) * 40
                efficiency = round(completion_score + overdue_score, 1)

            executor_stats.append({
                'executor__username': executor.username,
                'executor__first_name': executor.first_name,
                'executor__last_name': executor.last_name,
                'executor__get_full_name': str(executor),
                'total': total_user,
                'completed': completed_user,
                'in_progress': in_progress_user,
                'overdue': overdue_user,
                'completion_rate': round(completed_user / total_user * 100, 1) if total_user > 0 else 0,
                'efficiency': efficiency
            })

        executor_stats = sorted(executor_stats, key=lambda x: x['efficiency'], reverse=True)

    refresh = RefreshToken.for_user(user)
    context = {
        'tasks': tasks,
        'tasks_new': tasks.filter(status='new'),
        'tasks_in_progress': tasks.filter(status='in_progress'),
        'tasks_done': tasks.filter(status='done'),
        'stat_total': total,
        'stat_completed': completed,
        'stat_in_progress': in_progress,
        'stat_new': new_count,
        'stat_overdue': overdue,
        'stat_priority_low': priority_low,
        'stat_priority_medium': priority_medium,
        'stat_priority_high': priority_high,
        'user_role': user.role,
        'executor_stats': executor_stats,
        'show_analytics': user.role in ['admin', 'manager'],
        'jwt_access': str(refresh.access_token),
        'jwt_refresh': str(refresh),
    }

    return render(request, 'dashboard.html', context)

# ===================== TASK STATUS =====================

@login_required
def change_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.role == 'employee' and task.executor != request.user:
        messages.error(request, 'Нет прав')
        return redirect('/dashboard/')

    new_status = request.POST.get('next_status')

    if new_status in ['in_progress', 'done']:
        old = task.status
        task.status = new_status
        task.save()

        notify_status_changed(task, old, request.user)

        History.objects.create(
            task=task,
            changed_by=request.user,
            old_status=old,
            new_status=new_status
        )

    return redirect('/dashboard/')


# ===================== TASK CRUD =====================

@login_required
def task_create(request):
    if request.user.role == 'employee':
        return redirect('/dashboard/')

    projects = Project.objects.all()
    users = CustomUser.objects.all()

    if request.method == 'POST':
        from datetime import datetime

        # Получаем deadline и обрабатываем пустое значение
        deadline_str = request.POST.get('deadline', '')
        deadline = None

        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                # Если формат не совпадает, пробуем другой
                try:
                    deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
                except ValueError:
                    messages.error(request, 'Неверный формат даты')
                    return redirect('/dashboard/')

        # Если deadline не указан, ставим значение по умолчанию (например, через 7 дней)
        if not deadline:
            from datetime import timedelta
            deadline = datetime.now() + timedelta(days=7)

        task = Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            status=request.POST.get('status'),
            priority=request.POST.get('priority'),
            deadline=deadline,
            executor_id=request.POST.get('executor'),
            author=request.user,
            project_id=request.POST.get('project') or None
        )

        co_ids = request.POST.getlist('co_executors')
        if co_ids:
            task.co_executors.set(co_ids)

        # добавляем участников в проект
        if task.project:
            task.project.members.add(task.executor)
            task.project.members.add(*CustomUser.objects.filter(id__in=co_ids))

        notify_task_assigned(task)

        messages.success(request, 'Задача успешно создана')
        return redirect('/dashboard/')

    return render(request, 'task_form.html', {
        'users': users,
        'projects': projects,
        'task': None
    })


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.role == 'employee':
        return redirect('/dashboard/')

    users = CustomUser.objects.all()
    projects = Project.objects.all()

    if request.method == 'POST':
        from datetime import datetime

        old_status = task.status

        # Обработка deadline
        deadline_str = request.POST.get('deadline', '')
        deadline = None

        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
                except ValueError:
                    deadline = task.deadline
        else:
            deadline = task.deadline

        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')
        task.priority = request.POST.get('priority')
        task.deadline = deadline
        task.executor_id = request.POST.get('executor')
        task.project_id = request.POST.get('project') or None
        task.save()

        co_ids = request.POST.getlist('co_executors')
        task.co_executors.set(co_ids)

        if task.project:
            task.project.members.add(task.executor)
            task.project.members.add(*CustomUser.objects.filter(id__in=co_ids))

        if old_status != task.status:
            notify_status_changed(task, old_status, request.user)

            History.objects.create(
                task=task,
                changed_by=request.user,
                old_status=old_status,
                new_status=task.status
            )

        messages.success(request, 'Задача успешно обновлена')
        return redirect('/dashboard/')

    return render(request, 'task_form.html', {
        'users': users,
        'projects': projects,
        'task': task
    })
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.role == 'employee':
        return redirect('/dashboard/')

    if request.method == 'POST':
        task.delete()

    return redirect('/dashboard/')


# ===================== PROJECTS =====================

@login_required
def projects_list(request):
    return render(request, 'projects_list.html', {
        'user_role': request.user.role
    })


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    refresh = RefreshToken.for_user(request.user)

    return render(request, 'project_detail.html', {
        'project': project,
        'user_role': request.user.role,
        'jwt_access': str(refresh.access_token),
        'jwt_refresh': str(refresh),
    })

@login_required
def project_create(request):
    if request.user.role == 'employee':
        return redirect('/projects/')

    managers = CustomUser.objects.filter(role='manager')

    if request.method == 'POST':
        from decimal import Decimal
        from task.notifications import notify_project_manager_assigned, notify_project_created

        def parse_decimal(value, default=0):
            if not value or value == '':
                return Decimal(default)
            try:
                return Decimal(str(value).replace(',', '.'))
            except:
                return Decimal(default)

        def parse_float(value, default=0):
            if not value or value == '':
                return default
            try:
                return float(str(value).replace(',', '.'))
            except:
                return default

        # Определяем менеджера
        manager_id = request.POST.get('manager')
        manager = None
        if manager_id and request.user.role == 'admin':
            try:
                manager = CustomUser.objects.get(id=manager_id, role='manager')
            except CustomUser.DoesNotExist:
                pass
        elif request.user.role == 'manager':
            manager = request.user

        project = Project.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            client=request.POST.get('client', ''),
            contract_number=request.POST.get('contract_number', ''),
            budget=parse_decimal(request.POST.get('budget'), 0),
            planned_hours=parse_float(request.POST.get('planned_hours'), 0),
            start_date=request.POST.get('start_date') or None,
            end_date=request.POST.get('end_date') or None,
            color=request.POST.get('color', '#667eea'),
            tags=request.POST.get('tags', ''),
            manager=manager,
            status='active'
        )

        # Добавляем создателя в участники
        project.members.add(request.user)

        # Если менеджер назначен, добавляем его в участники и отправляем уведомление
        if manager:
            project.members.add(manager)
            # ========== ОТПРАВЛЯЕМ УВЕДОМЛЕНИЕ МЕНЕДЖЕРУ ==========
            notify_project_manager_assigned(project, manager)

        # ========== ОТПРАВЛЯЕМ УВЕДОМЛЕНИЕ СОЗДАТЕЛЮ ПРОЕКТА ==========
        notify_project_created(project, request.user)

        messages.success(request, f'Проект "{project.name}" успешно создан')
        if manager:
            messages.info(request, f'Менеджер {manager.username} назначен на проект')

        return redirect('/projects/')

    return render(request, 'project_form.html', {
        'managers': managers,
        'user_role': request.user.role
    })


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user.role == 'employee':
        return redirect('/projects/')

    if request.user.role == 'manager' and project.manager != request.user:
        messages.error(request, 'Вы можете редактировать только свои проекты')
        return redirect('/projects/')

    managers = CustomUser.objects.filter(role='manager')

    if request.method == 'POST':
        from decimal import Decimal
        from task.notifications import notify_project_manager_assigned

        def parse_decimal(value, default=0):
            if not value or value == '':
                return Decimal(default)
            try:
                return Decimal(str(value).replace(',', '.'))
            except:
                return Decimal(default)

        def parse_float(value, default=0):
            if not value or value == '':
                return default
            try:
                return float(str(value).replace(',', '.'))
            except:
                return default

        # Сохраняем старого менеджера для сравнения
        old_manager = project.manager

        project.name = request.POST.get('name')
        project.description = request.POST.get('description')
        project.client = request.POST.get('client', '')
        project.contract_number = request.POST.get('contract_number', '')
        project.budget = parse_decimal(request.POST.get('budget'), 0)
        project.planned_hours = parse_float(request.POST.get('planned_hours'), 0)
        project.start_date = request.POST.get('start_date') or None
        project.end_date = request.POST.get('end_date') or None
        project.color = request.POST.get('color', '#667eea')
        project.tags = request.POST.get('tags', '')
        project.status = request.POST.get('status', 'active')

        # Только админ может менять менеджера
        if request.user.role == 'admin':
            manager_id = request.POST.get('manager')
            new_manager = None
            if manager_id:
                try:
                    new_manager = CustomUser.objects.get(id=manager_id, role='manager')
                except CustomUser.DoesNotExist:
                    pass

            # Если менеджер изменился
            if new_manager != old_manager:
                project.manager = new_manager

                # Отправляем уведомление новому менеджеру
                if new_manager:
                    notify_project_manager_assigned(project, new_manager)

                    # Добавляем нового менеджера в участники
                    project.members.add(new_manager)

                # Можно также отправить уведомление старому менеджеру (опционально)
                # if old_manager:
                #     notify_project_manager_removed(project, old_manager)

        project.save()

        # Обновляем участников проекта
        if project.manager:
            project.members.add(project.manager)

        messages.success(request, f'Проект "{project.name}" успешно обновлён')
        return redirect(f'/projects/{project.id}/')

    return render(request, 'project_edit.html', {
        'project': project,
        'managers': managers,
        'user_role': request.user.role
    })
@login_required
def project_analytics(request, project_id):
    """Аналитика проекта"""
    from task.models import Project
    from task.views import ProjectViewSet
    from rest_framework.request import Request as DRFRequest

    project = get_object_or_404(Project, id=project_id)

    # Проверка прав доступа
    if request.user.role == 'employee' and request.user not in project.members.all():
        messages.error(request, 'У вас нет доступа к аналитике этого проекта')
        return redirect('/projects/')

    # Создаём DRF Request с нашим пользователем
    drf_request = DRFRequest(request)
    drf_request.user = request.user

    # Создаём viewset и передаём request
    viewset = ProjectViewSet()
    viewset.request = drf_request
    viewset.kwargs = {'pk': project_id}

    # Вызываем метод analytics
    response = viewset.analytics(drf_request, pk=project_id)

    # Добавляем дополнительные данные в контекст
    context = response.data
    context['user_role'] = request.user.role
    context['project'] = project

    return render(request, 'project_analytics.html', context)