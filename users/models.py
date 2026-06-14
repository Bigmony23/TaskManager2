from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('manager', 'Менеджер'),
        ('employee', 'Исполнитель'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    patronymic = models.CharField(max_length=20, blank=True, verbose_name='Отчество')

    def __str__(self):
        # Если имя и фамилия пустые, показываем username
        if self.first_name or self.last_name:
            return f'{self.last_name} {self.first_name}  {self.patronymic}'.strip()
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name} {self.patronymic}'