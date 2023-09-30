from .models import User
from .serializers import UserSerializer
from rest_framework import generics, permissions


class UserListView(generics.ListAPIView):
    # output a list of users
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # fields for filtering the list of users
    filterset_fields = {
        "age": ["exact", "lt", "gt", "lte", "gte"],
        "nationality": ["exact", "icontains"]
    }
    # fields for sorting the list of users
    ordering_fields = ['age', 'nationality']


class UserDetailView(generics.RetrieveAPIView):
    # output of user details
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserCreateView(generics.CreateAPIView):
    # create user
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserUpdateView(generics.UpdateAPIView):
    # update user data
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDeleteView(generics.DestroyAPIView):
    # delete user
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
