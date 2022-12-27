from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from .models import Post, Tag, Comment
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# Create your tests here.

class PostTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(username ='eralp',email="abc@abc.com", password="1234")
        me = User.objects.get(username="eralp")
        Post.objects.create(author= me, title ="Test the Test", text= "Testing the Test Works",upload='a')

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

    def test_is_password_username_valid(self):
        user = authenticate(username='sevval', password='1234')
        self.assertFalse(user)

    def test_search(self):
        me = User.objects.get(username="eralp")
        # Create a few test posts
        post1 = Post.objects.create(author=me,title="Test Post 1", text="This is the first test post",upload='x')
        post2 = Post.objects.create(author=me,title="Test Post 2", text="This is the second test post",upload='y')

        # Test searching for a query that matches the title of one of the posts
        searched = "Test Post 1"
        posts_s_ = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
        self.assertTrue(posts_s_.exists())
        self.assertEqual(posts_s_.count(), 1)
        self.assertEqual(posts_s_.first(), post1)

        searched = "Test Post 2"
        posts_s_ = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
        self.assertTrue(posts_s_.exists())
        self.assertEqual(posts_s_.count(), 1)
        self.assertEqual(posts_s_.first(), post2)

        searched = "test"
        posts = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
        self.assertTrue(posts.exists())
        self.assertEqual(posts.count(), 3)

        searched = "eralp"
        posts = Post.objects.filter(Q(title__icontains=searched) | Q(text__icontains=searched))
        self.assertFalse(posts.exists())
        self.assertEqual(posts.count(), 0)


class TagTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name="django")
        Tag.objects.create(name="Test Tag")

    def test_tags_have_names(self):
        django_tag = Tag.objects.get(name="django")
        test_tag = Tag.objects.get(name="Test Tag")
        self.assertEqual(django_tag.name, "django")
        self.assertFalse(test_tag.name, "da_jango")


class CommentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='user_A',
            password='password123'
        )
        Comment.objects.create(
            author=user,
            text='Django is Nice'
        )

    def test_comment_has_author(self):
        comment = Comment.objects.get(text='Django is Nice')
        self.assertEqual(comment.author.username, 'user_A')

    def test_comment_has_text(self):
        comment = Comment.objects.get(text='Django is Nice')
        self.assertEqual(comment.text, 'Django is Nice')


class ProfileEditTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.form_data = {'date_of_birth_date': '1900-01-01'}

    def test_form_valid(self):
        form = ProfileEditForm(self.form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_form_update(self):
        form = ProfileEditForm(self.form_data, instance=self.user)
        form.save()
        self.user.refresh_from_db()
        self.assertFalse(self.user.profile.birth_date, '1990-01-01')