from django.urls import path

from score.api.v1 import views

app_name = 'score-v1'

urlpatterns = [
    path('sessions/', views.SessionListCreateAPIView.as_view(), name='session-list-create'),
    path('sessions/<int:pk>/', views.SessionRetrieveUpdateDestroyAPIView.as_view(), name='session-rud'),
    path('sessions/<int:pk>/invite/', views.SessionInviteListCreateAPIView.as_view(), name='session-invite'),
]
