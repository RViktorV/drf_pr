from rest_framework import viewsets
from django.contrib.auth.models import User
from users.serializers import UsersSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
