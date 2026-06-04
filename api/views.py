from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from api.serializers import TaskSerializer
from task.models import Task


class TaskRetrieveViewSet(viewsets.ModelViewSet):
   serializer_class = TaskSerializer
   queryset = Task.objects.all()

   filter_backends = [DjangoFilterBackend]
   filterset_fields = ['status', 'priority', 'executor', 'author']
   def get_queryset(self):
      user = self.request.user

      if user.role == 'admin':
         return Task.objects.all()
      if user.role == 'manager':
          return Task.objects.filter(author=user)
      if user.role == 'employee':
         return Task.objects.filter(executor=user)
      return Task.objects.none()

   def perform_create(self, serializer):
      if self.request.user.role == 'employee':
         raise PermissionDenied("Недостаточно прав")
      serializer.save(author=self.request.user)





# Create your views here.
