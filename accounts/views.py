from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from accounts.forms import UserCreationForm


class UserView(DetailView):
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        user = self.request.user
        data = super(UserView, self).get_context_data(**kwargs)
        data['title'] = f'Профиль пользователя {user.get_short_name() or user.email}'
        return data


def signup(request):
    if request.method == 'POST':
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
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form, 'title': 'Регистрация'})
