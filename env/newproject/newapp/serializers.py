from rest_framework import serializers
from .models import  *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth.models import Group
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class CameraFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraFeed
        fields = '__all__'

class SystemConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfiguration
        fields = '__all__'

class EventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = '__all__'

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
      
        user_roles = UserRole.objects.filter(user=user)
        is_admin = user_roles.filter(role__name='admin').exists()
        is_super_admin = user_roles.filter(role__name='super_admin').exists()
        
        token['is_admin'] = is_admin
        token['is_super_admin'] = is_super_admin
        token['websocket_url'] = 'http://127.0.0.1:8000/api/stream/'  # Update this URL accordingly

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
      
        user_roles = UserRole.objects.filter(user=self.user)
        is_admin = user_roles.filter(role__name='admin').exists()
        is_super_admin = user_roles.filter(role__name='super_admin').exists()
        
       
        data.update({
            'is_admin': is_admin,
            'is_super_admin': is_super_admin,
            'websocket_url': 'http://127.0.0.1:8000/api/stream/',  # Update this URL accordingly
        })

        return data