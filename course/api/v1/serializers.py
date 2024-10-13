from rest_framework import serializers
from django.shortcuts import get_object_or_404

from user.models import User
from course.models import Course, Hole


class CourseIdURLParam:
    """
    Used to fetch the course object from the URL parameter. Similar to CurrentUserDefault.
    """

    requires_context = True

    def __call__(self, serializer_field) -> Course:
        return get_object_or_404(Course.objects.only('id'), id=serializer_field.context['view'].kwargs.get('course_id'))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'


class SmallCourseSerializer(serializers.ModelSerializer):
    """
    Generally used as a nested serializer for other serializers.
    """

    class Meta:
        model = Course
        fields = ('id', 'name', 'images', 'is_public')


class CourseSerializer(serializers.ModelSerializer):
    added_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = '__all__'


class HoleSerializer(serializers.ModelSerializer):
    """
    Generic repr for Hole model. Not used for writable purposes.
    """

    class Meta:
        model = Hole
        exclude = ('id', 'course')


class CourseWithHolesSerializer(serializers.ModelSerializer):
    """
    Lists holes for a course. Mostly used for read-only purposes.
    """

    holes = HoleSerializer(many=True, read_only=True)
    added_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = '__all__'


class HoleWriteSerializer(serializers.ModelSerializer):

    course = serializers.HiddenField(default=CourseIdURLParam())

    def create(self, validated_data: dict[str, int | Course]) -> Hole:
        course: Course = validated_data['course']
        user: User = self.context['request'].user

        if course.added_by != user:
            raise serializers.ValidationError('You can only add holes to courses you create.')

        return super().create(validated_data)

    class Meta:
        model = Hole
        fields = '__all__'
