from django.test import TestCase
from django.urls import reverse, resolve
from ShiftManagementApp.views import home,Login

class TestUrls(TestCase):

    def test_get_index_url(self):
        """ログインページにアクセスした時にfunction:Loginを解決できるか"""
        view = resolve('/login/')
        self.assertEqual(view.func,Login)