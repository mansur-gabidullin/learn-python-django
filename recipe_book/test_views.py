from django.test import TestCase, Client
from mixer.backend.django import mixer

from accounts.models import User
from recipe_book.models import Recipe


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def check_disallowed_methods(self, url, test_status, *methods):
        statuses = []

        for method in methods:
            request = getattr(self.client, method)(url)
            statuses.append(request.status_code)

        self.assertTrue(all((status == test_status for status in statuses)))

    def test_IndexView(self):
        response = self.client.get('/')
        self.assertEqual('Главная', response.context['title'])
        self.assertEqual(response.status_code, 200)
        self.check_disallowed_methods('/', 405, 'post', 'put', 'patch', 'delete', 'options')

    def test_RecipesListView(self):
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Рецепты', response.context['title'])
        self.assertIn('recipes', response.context)
        self.check_disallowed_methods('/recipes/', 405, 'post', 'put', 'patch', 'delete', 'options')

    def test_AboutAsTemplateView(self):
        response = self.client.get('/about_us/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('О нас', response.context['title'])
        self.check_disallowed_methods('/about_us/', 405, 'post', 'put', 'patch', 'delete', 'options')

    def test_RecipeFormView(self):
        recipe = mixer.blend(Recipe)

        self.check_disallowed_methods(f'/recipe/add/', 302, 'put', 'patch', 'delete', 'options')
        self.check_disallowed_methods(f'/recipe/view/{recipe.id}', 405, 'put', 'patch', 'delete', 'options')
        self.check_disallowed_methods(f'/recipe/edit/{recipe.id}', 302, 'put', 'patch', 'delete', 'options')
        self.check_disallowed_methods(f'/recipe/delete/{recipe.id}', 302, 'put', 'patch', 'delete', 'options')

        response = self.client.get(f'/recipe/view/{recipe.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(f'Просмотр рецепта {recipe.title}', response.context['title'])

        email = 'fake@email'
        password = 'fake_password'
        User.objects.create_user(email, password)

        self.client.login(email=email, password=password)
        response = self.client.get(f'/recipe/edit/{recipe.id}')
        self.assertEqual(response.status_code, 403)

        admin_email = 'admin_fake@email'
        admin_password = 'admin_fake_password'
        User.objects.create_superuser(admin_email, admin_password)
        self.client.login(email=admin_email, password=admin_password)

        response = self.client.get(f'/recipe/edit/{recipe.id}')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(f'Редактирование рецепта {recipe.title}', response.context['title'])
        self.assertIn('recipe', response.context)

        response = self.client.get(f'/recipe/delete/{recipe.id}')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(f'Удаление рецепта {recipe.title}', response.context['title'])

        previous_title = recipe.title

        response = self.client.post(f'/recipe/edit/{recipe.id}', {
            'title': 'new title',
            'description': 'new description',
            'ingredients': 'new ingredient',
            'steps': 'new step',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/recipes/')
        self.assertNotEqual(Recipe.objects.get(pk=recipe.id).title, previous_title)

        response = self.client.post(f'/recipe/delete/{recipe.id}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/recipes/')
        self.assertEqual(Recipe.objects.count(), 0)

        response = self.client.get(f'/recipe/add/{recipe.id}')
        self.assertEqual(response.status_code, 200)

        self.assertEqual('Добавление рецепта', response.context['title'])

        response = self.client.post(f'/recipe/add/', {
            'title': 'new title',
            'description': 'new description',
            'ingredients': 'new ingredient',
            'steps': 'new step',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/recipes/')
        self.assertEqual(Recipe.objects.count(), 1)

    def test_UserView(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)

        email = 'fake@email'
        password = 'fake_password'
        User.objects.create_user(email, password)
        self.client.login(email=email, password=password)

        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].email, email)
        self.assertEqual(f'Профиль пользователя {email}', response.context['title'])
        self.check_disallowed_methods('/accounts/profile/', 405, 'post', 'put', 'patch', 'delete', 'options')

    def test_signup(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Recipe.objects.count(), 0)

        email = 'fake@email.test'
        password = '8oKeIDot0^z1'

        response = self.client.post('/accounts/signup/', {
            'email': email,
            'password1': password,
            'password2': password,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/profile/')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(pk=1).email, email)

        self.check_disallowed_methods('/accounts/signup/', 405, 'put', 'patch', 'delete', 'options')
