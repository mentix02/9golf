from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.authtoken.views import ObtainAuthToken as BaseObtainAuthToken

from user.models import User
from user.api.v1.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """
    Creates a new user.
    """

    name = 'User Create API'

    queryset = User.objects.none()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class ObtainAuthTokenAPIView(BaseObtainAuthToken):
    """
    Custom ObtainAuthToken view that returns some user data.
    """

    name = 'Obtain Auth Token API'

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer)

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username, 'avatar': user.avatar})
