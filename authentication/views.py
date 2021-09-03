from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsAdmin
from .serializers import (AuthenticationTokenSerializer,
                          RegistrationUserSerializer, UserSerializer)

User = get_user_model()


class RegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationUserSerializer
    queryset = User.objects.all()


class AuthUserTokenView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = AuthenticationTokenSerializer
    queryset = User.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'username',
    ]

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = get_object_or_404(User, email=request.user.email)
        serializer = UserSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
