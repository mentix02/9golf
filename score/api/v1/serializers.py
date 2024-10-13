from rest_framework import serializers

from score.models import Session
from course.api.v1.serializers import SmallCourseSerializer
from user.api.v1.serializers import UserPublicSerializer as UserSerializer


class SessionSerializer(serializers.ModelSerializer):

    course = SmallCourseSerializer()
    player_count = serializers.SerializerMethodField()

    @staticmethod
    def get_player_count(session: Session) -> int:
        return (
            getattr(session, Session.PLAYER_COUNT_ANNOTATION)
            if hasattr(session, Session.PLAYER_COUNT_ANNOTATION)
            else session.users.count()
        )

    class Meta:
        model = Session
        fields = ('id', 'course', 'timestamp', 'player_count')


class SessionWriteSerializer(serializers.ModelSerializer):
    added_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Session
        exclude = ('users', 'session_users')  # noqa


class SessionSerializerWithUsers(SessionSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Session
        fields = SessionSerializer.Meta.fields + ('users',)
