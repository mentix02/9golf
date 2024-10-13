from typing import Type

from django.db.models.aggregates import Count

from rest_framework import generics
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated

from score.models import Session
from course.api.v1.serializers import SmallCourseSerializer
from score.api.v1.serializers import SessionSerializer, SessionWriteSerializer, SessionSerializerWithUsers


class SessionListCreateAPIView(generics.ListCreateAPIView):

    name = 'Session List Create API'

    only_fields = ('id', 'course', 'timestamp', 'added_by') + tuple(
        f'course__{field}' for field in SmallCourseSerializer.Meta.fields
    )

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self) -> Type[ModelSerializer]:
        return SessionWriteSerializer if self.request.method == 'POST' else SessionSerializer

    def get_queryset(self):
        return (
            self.request.user.created_sessions.all()
            .select_related('course')
            .only(*self.only_fields)
            .annotate(**{Session.PLAYER_COUNT_ANNOTATION: Count('users')})
        )


class SessionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    name = 'Session Retrieve Update Destroy API'

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self) -> Type[ModelSerializer]:
        match self.request.method:
            case 'GET':
                return SessionSerializerWithUsers
            case 'DELETE':
                return SessionSerializer
            case 'PUT' | 'PATCH':
                return SessionWriteSerializer
            case _:
                raise ValueError(f'Unsupported method: {self.request.method}')

    def get_queryset(self):
        return (
            self.request.user.created_sessions.all()
            .annotate(**{Session.PLAYER_COUNT_ANNOTATION: Count('users')})
            .prefetch_related('users')
        )


class SessionInviteListCreateAPIView(generics.ListCreateAPIView):

    name = 'Session Invite API'

    serializer_class = SessionSerializerWithUsers
    permission_classes = (IsAuthenticated,)
    queryset = Session.objects.all()
