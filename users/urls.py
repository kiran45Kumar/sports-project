from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UsersViewSet)
router.register(r'admin', AdminViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin_user/', AdminLogin.as_view(),name='admin_user'),
    path('login_user/', LoginUser.as_view(),name='login_user'),
    path('approve_user/', ApproveUser.as_view(),name='approve_user'),
    path('reject_user/', RejectUser.as_view(),name='reject_user'),
    path('send_email/', SendEmail.as_view(),name='send_email'),
    path('reset_password/', ResetPassword.as_view(),name='reset_password'),
    path('signup_user/', RegisterUser.as_view(),name='signup_user'),
    path('login/', Login.as_view(),name='login'),
    path('logout_user/', LogoutUser.as_view(),name='logout_user'),
]
