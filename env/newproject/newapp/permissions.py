# from rest_framework import permissions
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from .models import CameraFeed, SystemConfiguration, EventLog
# from .serializers import CameraFeedSerializer, SystemConfigurationSerializer, EventLogSerializer
# from .permissions import IsSuperAdmin, IsAdmin
# class IsSuperAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
       
#         return request.user.userrole_set.filter(role__name='super_admin').exists()

# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):

#         return request.user.userrole_set.filter(role__name='admin').exists()


# class CameraFeedViewSet(viewsets.ModelViewSet):
#     queryset = CameraFeed.objects.all()  # Assuming you have a CameraFeed model
#     serializer_class = CameraFeedSerializer
#     permission_classes = [IsAuthenticated, IsAdmin]  # Admins can view camera feeds

# class SystemConfigurationViewSet(viewsets.ModelViewSet):
#     queryset = SystemConfiguration.objects.all()  # Assuming you have a SystemConfiguration model
#     serializer_class = SystemConfigurationSerializer
#     permission_classes = [IsAuthenticated, IsSuperAdmin]  # Super Admins can access system configurations

# class EventLogViewSet(viewsets.ModelViewSet):
#     queryset = EventLog.objects.all()  
#     serializer_class = EventLogSerializer
#     permission_classes = [IsAuthenticated, IsSuperAdmin]  # Super Admins can view logs
from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.userrole_set.filter(role__name='super_admin').exists()

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.userrole_set.filter(role__name='admin').exists()