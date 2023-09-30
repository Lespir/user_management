from django.urls import path
from .apiview import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<str:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users_create/', UserCreateView.as_view(), name='user_create'),
    path('users_update/<str:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users_delete/<str:pk>/', UserDeleteView.as_view(), name='user_delete')
]
