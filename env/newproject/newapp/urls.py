from django.urls import path
from .views import *
from .views import stream_view
camera_feed_list = CameraFeedViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

camera_feed_detail = CameraFeedViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
          path('api/users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
          path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
          path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
          path('stream/', stream_view, name='stream_view'),
          path('camera-feeds/', camera_feed_list, name='camera-feed-list'),
          path('camera-feeds/<int:pk>/', camera_feed_detail, name='camera-feed-detail'),
   
]




