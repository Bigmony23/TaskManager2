from rest_framework import serializers
from .models import CustomUser

from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'patronymic', 'full_name', 'role', 'date_joined']
        read_only_fields = ['date_joined']

    def get_full_name(self, obj):
        return str(obj)