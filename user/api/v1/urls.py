from django.urls import path

from user.api.v1 import views

app_name = 'user-v1'

urlpatterns = [
    path('create/', views.UserCreateAPIView.as_view(), name='create'),
    path('token/', views.ObtainAuthTokenAPIView.as_view(), name='token'),
]
