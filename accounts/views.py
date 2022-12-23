import logging

from django.contrib.auth import authenticate, login
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from rest_framework.authtoken.models import Token

from accounts.forms import UserCreationForm

logger = logging.getLogger("django.request")


class UserView(DetailView):
    template_name = 'accounts/profile.html'
    http_method_names = ['get']

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        user = self.request.user
        data = super(UserView, self).get_context_data(**kwargs)
        data['title'] = f'Профиль пользователя {user.get_short_name() or user.email}'
        return data


def signup(request):
    match request.method:
        case 'POST':
            form = UserCreationForm(request.POST)

            if form.is_valid():
                user = form.save()
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(request, email=user.email, password=raw_password)

                if user is not None:
                    login(request, user)
                else:
                    print("user is not authenticated")

                return redirect('accounts:profile')
        case 'GET':
            form = UserCreationForm()

        case _:
            logger.warning(
                "Method Not Allowed (%s): %s",
                request.method,
                request.path,
                extra={"status_code": 405, "request": request},
            )

            return HttpResponseNotAllowed(['GET', 'POST'])

    return render(request, 'accounts/signup.html', {'form': form, 'title': 'Регистрация'})


def update_token_ajax(request):
    is_post = request.method == 'POST'

    if not is_post:
        return HttpResponseNotAllowed(['POST'])

    user = request.user
    token = None

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        ...

    if token:
        token.delete()

    token = Token.objects.create(user=user)

    return JsonResponse({'key': token.key})
