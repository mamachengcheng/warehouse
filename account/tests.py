from django.test import TestCase
from django.test import Client
from .models import Account,Announcement

# Create your tests here.
class LoginUrlTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_get(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post(self):
        # response = self.client.post('/login/', {'username':'admin','password':'123'})
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'login.html')
        # self.assertEqual(response.status_code, 301)
        # self.assertRedirects(response, '/login/')
        response = self.client.post('/login/', {'username':'admin','password':'admin123'})
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, '/backend/')
        # self.assertTemplateUsed(response, 'backend.html')

    def test_announcement_url(self):
        response = self.client.get('/announcement_list/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/announcement_list/')
        response = self.client.get('/announcement_list/list/')
        self.assertEqual(response.status_code, 404)

        # self.assertTemplateUsed(response, 'login.html')

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        Account.objects.create_user(username='test', password='test123')
        Announcement.objects.create(id=1,title='测试公告',status=1)
        self.client.login(username='test', password='test123')


    def test_account_login(self):
        response = self.client.get('/announcement_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'announcement_list.html')
        response = self.client.get('/announcement_edit/1/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
        response = self.client.post('/announcement_del/1/',)
        self.assertEqual(response.status_code, 403)
