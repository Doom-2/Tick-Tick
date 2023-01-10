from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from core.models import User
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
    UpdateAPIView
)
from core.serializers import (
    RegisterSerializer,
    UserDetailsSerializer,
    LoginSerializer,
    ChangePasswordSerializer
)


@api_view(['GET'])
def health_check(request):
    return Response({'status': 'Ok'})


# Create a new user
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# Get user profile
class UserProfile(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        user_id = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, user_id)
        return user_id

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response('Logged out', status=status.HTTP_204_NO_CONTENT)


class UserLoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        login(request, user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            elif serializer.data.get('old_password') == serializer.data.get('new_password'):
                return Response({'new_password': ["Can't be the same."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return JsonResponse(response, status=200)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
