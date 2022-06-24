from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UsersSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """create a new user in the system"""
    serializer_class = UsersSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """"Manage the authenticated user"""
    serializer_class = UsersSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """retrieve and return authenticated user"""
        return self.request.user
