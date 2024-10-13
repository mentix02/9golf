from django.urls import path

from course.api.v1 import views

app_name = 'course-v1'

urlpatterns = [
    path('', views.CourseListCreateAPIView.as_view(), name='list-create'),
    path('<int:pk>/', views.CourseRetrieveAPIView.as_view(), name='retrieve'),
    path('edit/<int:pk>/', views.CourseRetrieveUpdateDestroyAPIView.as_view(), name='edit'),
    path('edit/<int:course_id>/holes/', views.CourseHoleListCreateAPIView.as_view(), name='holes'),
]
