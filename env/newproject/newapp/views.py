import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import render
from .models import *
from .serializers import *
from .permissions import IsSuperAdmin, IsAdmin


logger = logging.getLogger('newproject')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @action(detail=True, methods=['post'])
    def assign_role(self, request, pk=None):
        user = self.get_object()
        role_id = request.data.get('role_id')
        try:
            role = Role.objects.get(id=role_id)
            UserRole.objects.create(user=user, role=role)
            logger.info(f"Role '{role.name}' assigned to user '{user.username}' by {request.user.username}")
            return Response({'status': 'role assigned'})
        except Role.DoesNotExist:
            logger.error(f"Role ID {role_id} not found for user {request.user.username}")
            return Response({'error': 'Role not found'}, status=status.HTTP_400_BAD_REQUEST)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ObtainTokenView(TokenObtainPairView):
    pass

class RefreshTokenView(TokenRefreshView):
    pass

class CameraFeedViewSet(viewsets.ModelViewSet):
    queryset = CameraFeed.objects.all()
    serializer_class = CameraFeedSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsSuperAdmin]
        else:
            self.permission_classes = [IsAdmin]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)
        logger.info(f"Camera feed '{serializer.instance.name}' added by {self.request.user.username}")
        EventLog.objects.create(
            event_type='info',
            message=f'Camera feed {serializer.instance.name} added by {self.request.user.username}',
            user=self.request.user
        )

class SystemConfigurationViewSet(viewsets.ModelViewSet):
    queryset = SystemConfiguration.objects.all()
    serializer_class = SystemConfigurationSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f"System configuration '{serializer.instance.key}' updated by {self.request.user.username}")
        EventLog.objects.create(
            event_type='info',
            message=f'System configuration {serializer.instance.key} updated by {self.request.user.username}',
            user=self.request.user
        )

class EventLogViewSet(viewsets.ModelViewSet):
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

def stream_view(request):
    logger.info(f"Stream view accessed by {request.user.username}")
    return render(request, 'stream.html')
