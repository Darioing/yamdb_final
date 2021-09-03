from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuthUserTokenView, RegistrationView, UserViewSet

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, 'Users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', AuthUserTokenView, name='Authenticaton_User'),
    path('v1/auth/email/', RegistrationView, name='Registration_User'),
]
