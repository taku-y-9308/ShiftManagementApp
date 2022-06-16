import datetime
from lib2to3.pgen2.tokenize import tokenize
from urllib import response
from django.test import TestCase
from django.urls import reverse, resolve
from ShiftManagementApp.views import home
from ShiftManagementApp.models import User,UserManager,Shift

class LoginpageTest(TestCase):
    def test_get_status_code_index(self):
        """ログインページにアクセスしたときのステータスコードが200であることを確認"""
        response = self.client.get(reverse('ShiftManagementApp:Login'))
        self.assertEqual(response.status_code,200)

class Calendartest(TestCase):
    def setUp(self):
        """テストログイン用ユーザを作成してログイン維持する"""
        shop_id = 0
        username = 'testuser'
        default_position = True
        email = 'test@mail.com'
        password = 'testpassword'
        is_edit_mode = True

        self.user = User.objects.create_user(
            username,
            email,
            password,
            shop_id=shop_id,
            default_position=default_position,
            is_edit_mode=is_edit_mode
            )

        self.client.login(email=email,password=password)

    def test_response_code_get_indexpage(self):
        """homeページの表示したときのレスポンスコードが200かどうか確認"""
        response = self.client.get(reverse('ShiftManagementApp:index'))
        self.assertEqual(response.status_code,200)
    
    def test_response_code_post_calendar(self):
        """シフト提出したときのレスポンスコードが200かどうか確認"""
        post_data = {
            "id" : 1,
            "date":"2022-07-01",
            "start":"12:00",
            "end":"18:00",
        }
        response = self.client.post(reverse('ShiftManagementApp:SubmitShift-Ajax'),post_data,content_type='application/json')
        self.assertEqual(response.status_code,200)
    
    def test_check_database_post_calendar(self):
        """DBにデータを送信して正常に格納されているか確認"""
        post_data = {
            "id" : 1,
            "date":"2022-07-01",
            "start":"12:00",
            "end":"18:00",
        }
        response = self.client.post(reverse('ShiftManagementApp:SubmitShift-Ajax'),post_data,content_type='application/json')
        shift = Shift.objects.all()
        
        self.assertEqual(shift[0].date,datetime.date(2022, 7, 1))
        tz = datetime.timezone(datetime.timedelta(hours=0))
        self.assertEqual(shift[0].begin,datetime.datetime(2022, 7, 1, 3, 0, 0,tzinfo=tz))
        self.assertEqual(shift[0].finish,datetime.datetime(2022, 7, 1, 9, 0, 0,tzinfo=tz))