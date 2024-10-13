from typing import Any, Type, Callable

from rest_framework.request import Request
from rest_framework.permissions import BasePermission

from user.models import User


def create_user_owned_object_permission(owner_accessor: Callable[[Any], User]) -> Type[BasePermission]:
    """
    Some more convoluted shit going on here. Let me break it down.

    owner_accessor expects a function that can "traverse" an object to find the user instance
    associated with it. We use an "accessor" function since some objects may have to be "traversed"
    multiple layers before we find an "owner" field.

    Simplest example being a "Hole" instance - a hole has no associated owner - only a course.
    A course, however, DOES have a "added_by" field. Therefore, a "Hole" owner accessor may look
    something like this - lambda hole : hole.course.added_by

    A "Hole" specific permission would be built like -
        >>> create_user_owned_object_permission(lambda hole : hole.course.added_by)

    Fun meta-programming here.
    """

    class ObjectPermission(BasePermission):
        def has_object_permission(self, request: Request, view, obj) -> bool:
            return owner_accessor(obj) == request.user

    return ObjectPermission
