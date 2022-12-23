from django.contrib.auth.forms import UserCreationForm as _UserCreationForm, UserChangeForm as _UserChangeForm

from accounts.models import User


class UserCreationForm(_UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(_UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
