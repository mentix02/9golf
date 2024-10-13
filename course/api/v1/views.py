from django.db.models.query import Q, Prefetch
from django.db.models.fields import IntegerField
from django.db.models.expressions import Case, When, Value

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from course.models import Hole, Course
from user.permissions import create_user_owned_object_permission
from course.api.v1.serializers import CourseSerializer, HoleWriteSerializer, CourseWithHolesSerializer


class CourseListCreateAPIView(generics.ListCreateAPIView):

    name = 'Course List API'

    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            Course.objects.filter(Q(is_public=True) | Q(added_by=self.request.user))
            .annotate(
                is_added_by_user=Case(
                    When(added_by=self.request.user, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            .order_by('name')
            .order_by('-is_added_by_user')
        )


class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    name = 'Course Edit API'

    permission_classes = (IsAuthenticated,)
    serializer_class = CourseWithHolesSerializer

    def get_queryset(self):
        return Course.objects.filter(added_by=self.request.user).prefetch_related(
            Prefetch('holes', queryset=Hole.objects.order_by('number'))
        )


class CourseRetrieveAPIView(generics.RetrieveAPIView):

    name = 'Course Retrieve API'

    serializer_class = CourseWithHolesSerializer

    def get_queryset(self):
        return Course.objects.filter(is_public=True).prefetch_related(
            Prefetch('holes', queryset=Hole.objects.order_by('number'))
        )


class CourseHoleListCreateAPIView(generics.ListCreateAPIView):

    name = 'Course Hole List Create API'

    pagination_class = None
    serializer_class = HoleWriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Hole.objects.filter(course_id=self.kwargs.get('course_id')).order_by('number')
