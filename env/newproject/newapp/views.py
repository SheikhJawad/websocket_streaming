from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import render
from .models import User, Role, UserRole, CameraFeed, SystemConfiguration, EventLog
from .serializers import*
from .permissions import IsSuperAdmin, IsAdmin

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
            return Response({'status': 'role assigned'})
        except Role.DoesNotExist:
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
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)
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
    return render(request, 'stream.html')






