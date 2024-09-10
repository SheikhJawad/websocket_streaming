# from django.urls import path
# from . import views
# urlpatterns = [
    
# ]

# newapp/urls.py

from django.urls import path
from .views import *
from .views import stream_view

urlpatterns = [
    path('api/users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('stream/', views.stream_view, name='stream'),
      path('stream/', stream_view, name='stream_view'),
   
]

