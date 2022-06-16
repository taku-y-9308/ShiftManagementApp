from django.test import TestCase
from ShiftManagementApp.models import User

class PostModelTests(TestCase):
    
    def test_is_empty(self):
        """初期状態で何も登録されていない事を確認"""
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(),0)
    
    def test_is_count_one(self):
        """レコードを更新すると、レコードが１増えることを確認"""
        user = User.objects.create(
            shop_id = 0,
            username = 'testuser',
            default_position = True,
            email = 'test@mail.com'
        )
        saved_users = User.objects.all()
        self.assertEqual(saved_users.count(),1)
    
    def test_save_and_retrieving_user(self):
        """内容を指定してレコードを追加してすぐ取り出した時、同じものが取り出されるかを確認"""
        shop_id = 0
        username = 'testuser'
        default_position = True
        email = 'test@mail.com'

        user = User.objects.create(
            shop_id = shop_id,
            username = username,
            default_position = default_position,
            email = email
        )
        saved_user = User.objects.all()[0]

        self.assertEqual(saved_user.shop_id,shop_id)
        self.assertEqual(saved_user.username,username)
        self.assertEqual(saved_user.default_position,default_position)
        self.assertEqual(saved_user.email,email)

