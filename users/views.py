from rest_framework import viewsets

from users.models import Users
from users.serializers import UsersSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
