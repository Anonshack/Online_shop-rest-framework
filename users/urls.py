from django.urls import path
from .views import (
                    UserRegisterView,
                    UserLoginView,
                    UserDetailView,
                    UsersListView,
                    PasswordChangeView,
                    UserUpdateView,
                    Logout,
                    )

urlpatterns = [
    path('register', UserRegisterView.as_view()),
    path('login', UserLoginView.as_view()),
    path('users-detail', UserDetailView.as_view()),
    path('users-list', UsersListView.as_view()),
    path('change-password', PasswordChangeView.as_view(), name='change-password'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='updete-user'),
    path('logout', Logout.as_view(), name='logout'),
]