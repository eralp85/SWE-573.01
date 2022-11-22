from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your tests here.

class PostTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username ='eralp',email="abc@abc.com", password="1234")
        me = User.objects.get(username="eralp")
        Post.objects.create(author= me, title ="Test the Test", text= "Testing the Test Works")

    def test_post_exists(self):
        p = Post.objects.all()
        self.assertTrue(p.exists())

    def test_user_exists(self):
        me = User.objects.get(username='eralp')
        self.assertTrue(me)

    def test_user_login(self):
        user = authenticate(username='eralp', password='1234')
        self.assertTrue(user)

    def test_user_register(self):
        data = {

            'username': 'testuser',
            'email': 'abc@gmail.com',
            'password1': 'Eralp123!',
            'password2': 'Eralp123!',

        }

        form = UserCreationForm(data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_user_cannot_register_with_common_password(self):
        data = {

            'username': 'testuser',
            'email': 'abc@gmail.com',
            'password1': 'test123',
            'password2': 'test123',

        }

        form = UserCreationForm(data)

        self.assertFalse(form.is_valid())
        self.assertIn( "This password is too common.", form.errors.as_text())
        self.assertIn("This password is too short.", form.errors.as_text())