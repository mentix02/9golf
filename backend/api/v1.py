from django.urls import path, include

urlpatterns = [
    path('user/', include('user.api.v1.urls')),
    path('course/', include('course.api.v1.urls')),
    path('score/', include('score.api.v1.urls')),
]
