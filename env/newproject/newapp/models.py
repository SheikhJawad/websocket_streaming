from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        return self.create_user(username, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
   
    objects = CustomUserManager()

   
class Role(models.Model):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
    ]
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.get_name_display()

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles')

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

    class Meta:
        unique_together = ('user', 'role')





class CameraFeed(models.Model):
    CAMERA_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
    ]

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    feed_url = models.CharField(max_length=200)  # Change URLField to CharField
    status = models.CharField(
        max_length=20,
        choices=CAMERA_STATUS_CHOICES,
        default='inactive'
    )
    is_streaming = models.BooleanField(default=False)  # To control streaming
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='camera_feeds'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name} - {self.location}'


class SystemConfiguration(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.key}: {self.value}'


class EventLog(models.Model):
    EVENT_TYPE_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='info')
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='event_logs')
    system_info = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f'{self.timestamp} - {self.get_event_type_display()}: {self.message}'
