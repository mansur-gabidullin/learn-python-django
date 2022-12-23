# ViewSets define the view behavior.
from rest_framework import viewsets

from accounts.models import User
from accounts.serializers import UserSerializer

app_name = 'accounts'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
