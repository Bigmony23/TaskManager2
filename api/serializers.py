from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from task.models import Task
from users.models import CustomUser


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['author']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

