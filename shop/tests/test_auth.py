from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('shop:register')
        self.login_url = reverse('shop:login')
        self.logout_url = reverse('shop:logout')
        self.user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        }

    def test_registration_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/register.html')

    def test_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        # Check redirection to home
        self.assertRedirects(response, reverse('shop:home'))
        # Check user created
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        # Check user logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_registration_invalid_password_no_uppercase(self):
        data = self.user_data.copy()
        data['password'] = 'password123!'
        data['confirm_password'] = 'password123!'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200) # Should stay on page
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('Password must contain at least one uppercase letter.', str(form.errors))

    def test_login_view(self):
        # Create user first
        user = User.objects.create_user(username='testuser', email='test@example.com', password='Password123!')
        
        response = self.client.post(self.login_url, {
            'email': 'test@example.com',
            'password': 'Password123!'
        })
        self.assertRedirects(response, reverse('shop:home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_view(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='Password123!')
        self.client.login(username='testuser', password='Password123!')
        
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, reverse('shop:home'))
        response = self.client.get(reverse('shop:home'))
        self.assertFalse(response.context['user'].is_authenticated)
