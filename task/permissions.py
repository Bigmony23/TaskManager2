from rest_framework.permissions import BasePermission, SAFE_METHODS


class CanEditTask(BasePermission):
    """
    Role-based permission system:

    admin → full access
    manager → full access to own tasks (author) — create, edit, delete
    employee:
        - read own tasks
        - update ONLY status if executor or co-executor
        - NO delete
    """

    def has_permission(self, request, view):
        """Разрешение на уровне запроса (для списков и создания)"""
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Создание задачи (POST)
        if request.method == 'POST':
            # Admin и Manager могут создавать задачи
            return user.role in ['admin', 'manager']

        # Для остальных методов проверяем на уровне объекта
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # =========================
        # ADMIN
        # =========================
        if user.role == 'admin':
            return True

        # =========================
        # MANAGER
        # =========================
        if user.role == 'manager':
            # Менеджер может работать только со своими задачами
            if obj.author != user:
                return False

            # Разрешаем всё для своих задач: GET, PUT, PATCH, DELETE
            return True

        # =========================
        # EMPLOYEE
        # =========================
        if user.role == 'employee':
            # Чтение (GET, HEAD, OPTIONS)
            if request.method in SAFE_METHODS:
                return (
                    obj.executor == user or
                    obj.author == user or
                    obj.co_executors.filter(id=user.id).exists()
                )

            # Изменение (PATCH, PUT)
            if request.method in ['PATCH', 'PUT']:
                # Только изменение статуса
                allowed_fields = {'status'}
                if set(request.data.keys()) != allowed_fields:
                    return False

                # Только если он участник задачи
                return (
                    obj.executor == user or
                    obj.co_executors.filter(id=user.id).exists()
                )

            # Удаление (DELETE) — запрещено для исполнителя
            if request.method == 'DELETE':
                return False

        return False