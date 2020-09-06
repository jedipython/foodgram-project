from django.core import mail
from django.urls import reverse
from django.test import TestCase, Client
from users.views import SignUp, send_mail_ls
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from posts.models import Post, Group, Follow, Comment
import time
from django.contrib.auth.models import User
User = get_user_model()

    
class EmailTest(TestCase):
        def setUp(self):
                self.client = Client()
                self.user = self.client.post('/auth/signup/', {'username': 'jonni', 'password1': 'tuhatuhamaha6', 'password2': 'tuhatuhamaha6', 'email': 'pythonda@da.ru'})
                self.user = User.objects.get(username="jonni")
                self.client.force_login(self.user)

        def test_mail(self):
                
                # Автоотправка письма произошла после регистрации юзера
                # Проверяем, что письмо лежит в исходящих
                self.assertEqual(len(mail.outbox), 1)

        def test_Mail_Sub_jects(self):
                # Проверяем, что тема первого письма правильная.
                self.assertEqual(mail.outbox[0].subject, 'Подтверждение регистрации Yatube')
        
        def test_profile(self):
                response = self.client.get('/jonni/')
                self.assertAlmostEqual(response.status_code, 200)

        def test_newpost(self):
                self.client.login(username='jonni', password='bsdfgSD21123')
                response = self.client.get('/new/')
                self.assertAlmostEqual(response.status_code, 200)
                self.post = Post.objects.create(text="Всем привет, я временный ДЖонни, это мой первый пост, наф наф!", author=self.user)
                self.assertEqual((Post.objects.filter(author=self.user).count()), 1)
                response = self.client.get('/jonni/')
                self.assertEqual(len(response.context["page"]), 1)
                response = self.client.get('/')
                self.assertEqual(len(response.context["page"]), 1)
                
                response = self.client.get('/jonni/1/')
                self.assertEqual(response.status_code, 200)

                response = self.client.get(reverse('post_edit', kwargs={'username': 'jonni', 'post_id': '1'}),{'text': 'Edited text'})
                self.assertEqual(response.status_code, 200)
                

        def test_newpost_logout(self):
                self.client.logout()
                response = self.client.get('/new/')
                self.assertAlmostEqual(response.status_code, 302) # Проверяем, что на страницу создания поста нельзя зайти неавториз юзеру ,и его редиректит.

        def test_404(self):
                response = self.client.get('/ffsdfsfwefwefsc/')
                self.assertEqual(response.status_code, 404)


class ImageTests(TestCase):
        def setUp(self):
                self.client = Client()
                self.user = self.client.post('/auth/signup/', {'username': 'agent007', 'password1': 'tuhatuhamaha6', 'password2': 'tuhatuhamaha6', 'email': 'pythonda@da.ru'})
                self.user = User.objects.get(username="agent007")
                self.client.force_login(self.user)
                

        def test_image_post(self):
                with open('media/posts/starlink4_website_Qhna5v6.jpg', 'rb') as fp:
                        self.client.post('/new/', {'title': 'hello post', 'text': 'test post with image oh-ye', 'image': fp, 'author': 'agent007'})
                response = self.client.get('/agent007/1/')
                self.assertIn('<img', response.content.decode())
                time.sleep(21)
                response = self.client.get('/')
                self.assertIn('<img', response.content.decode())
                response = self.client.get('/agent007/')
                self.assertIn('<img', response.content.decode())
        
        def test_non_image(self):
                with open('ezample.txt', 'rb') as text_file:
                        self.client.post('/new/', {'text': 'test post2 with image oh-ye', 'image': text_file, 'author': 'agent007'})
                        response = self.client.get('/agent007/')
                        self.assertNotIn('<img', response.content.decode())
        
        def test_cache(self):
                self.client.post('/new/', {'text': 'test cache now', 'author': 'agent007'})
                time.sleep(7)
                response = self.client.get('/')
                self.assertNotIn('test cache now', response.content.decode())


class FollowTests(TestCase):
        def setUp(self):
                self.client = Client()
                self.user = self.client.post('/auth/signup/', {'username': 'agent007', 'password1': 'tuhatuhamaha6', 'password2': 'tuhatuhamaha6', 'email': 'pythonda@da.ru'})
                self.test_user1 = User.objects.create_user(username='testuser1', password='12345') 
                self.test_user1.save()
                self.test_user2 = User.objects.create_user(username='testuser2', password='12345') 
                self.test_user2.save()

        def test_follow(self): #проверяем, что человек может подписаться и отписаться от другого человека
                self.user = User.objects.get(username="testuser2")
                self.client.force_login(self.user)
                self.assertEqual((Follow.objects.filter(user=self.test_user2, author=self.test_user1.id).count()), 0) 
                response = self.client.get('/testuser1/follow')
                self.assertEqual((Follow.objects.filter(user=self.test_user2, author=self.test_user1.id).count()), 1) 
                response = self.client.get('/testuser1/unfollow')
                self.assertEqual((Follow.objects.filter(user=self.test_user2, author=self.test_user1.id).count()), 0) 

        def test_follow_posts(self): #проверяем, что подписанный человек может видеть посты своего кумира у себя в ленте, а когда отпишется от него - не может  + комментировать посты может только залогиненный юзер
                self.user = User.objects.get(username="testuser1")
                self.client.force_login(self.user)
                self.post = Post.objects.create(text="Всем привет, я пост проверки подписки, это  первый пост юзера testuser1, наф наф!", author=self.user)
                self.client.logout()

                self.user = User.objects.get(username="testuser2")
                self.client.force_login(self.user)
                response = self.client.get('/testuser1/follow')
                time.sleep(21)
                response = self.client.get('/follow/')
                self.assertIn('Всем привет, я пост проверки подписки', response.content.decode())
                response = self.client.get('/testuser1/unfollow')
                time.sleep(21)
                response = self.client.get('/follow/')
                self.assertNotIn('Всем привет, я пост проверки подписки', response.content.decode())

                response = self.client.get('/testuser1/1/')
                self.client.post('/testuser1/1/comment/', {'text': 'Оставляю тестовый комментарийe', 'author': 'testuser2'})
                response = self.client.get('/testuser1/1/')
                self.assertIn('Оставляю тестовый комментарий', response.content.decode())
                self.client.logout()
                response = self.client.get('/testuser1/1/')
                self.assertNotIn('Добавить комментарий', response.content.decode())





               
