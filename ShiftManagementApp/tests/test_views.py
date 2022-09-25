import datetime,json
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

class RedirectTest(TestCase):
    def test_redirect(self):
        """ログインせずにログイン必要なページにアクセスしたときにログインページにリダイレクトされるか"""
        response = self.client.get('/home/')
        self.assertRedirects(response,'/login/?next=/home/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)


class AllpageTest(TestCase):
    def setUp(self):
        """テストログイン用ユーザを作成してログイン維持する"""
        shop_id = 0
        username = 'testuser'
        default_position = True
        email = 'test@mail.com'
        password = 'testpassword'
        is_edit_mode = True
        is_active = True

        self.user = User.objects.create_user(
            username,
            email,
            password,
            shop_id=shop_id,
            default_position=default_position,
            is_edit_mode=is_edit_mode,
            is_active=is_active
            )

        self.client.login(email=email,password=password)

    def test_all_page_test(self):
        """url.pyに登録されているHTMLを返す全ページのレスポンスコードが200であることを確認"""
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/home/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/create-newaccount/')
        self.assertEqual(response.status_code,200)
        
        response = self.client.get('/submit-shift/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/edit-shift/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/line/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/shift-list/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/shift-list-print/')
        self.assertEqual(response.status_code,200)

        #設定画面のHTMLだけテスト、アカウントデータは下で検証
        response = self.client.get('/account-setting/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/password_reset/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/password_reset/done/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/reset/done/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code,200)

        response = self.client.get('/contact/done/')
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
        is_active = True

        self.user = User.objects.create_user(
            username,
            email,
            password,
            shop_id=shop_id,
            default_position=default_position,
            is_edit_mode=is_edit_mode,
            is_active=is_active
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
            "id" : 2,
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

class AccountSettingCheck(TestCase):
    def setUp(self):
        """テスト用管理ユーザを作成してログイン維持する"""
        shop_id = 0
        username = 'admin_testuser'
        default_position = True
        email = 'admin_testuser@mail.com'
        password = 'admintestpassword'
        is_edit_mode = True
        is_active = True
        is_staff = True

        self.user = User.objects.create_user(
            username,
            email,
            password,
            shop_id=shop_id,
            default_position=default_position,
            is_edit_mode=is_edit_mode,
            is_active=is_active,
            is_staff=is_staff
            )
        #テスト用一般ユーザーを作成
        self.user = User.objects.create_user(
            'testuser',
            'tesetuser@mail.com',
            'testpassword',
            shop_id=0,
            default_position=False,
            is_edit_mode=False,
            is_active=True,
            is_staff=False
        )
        
        #管理ユーザーでログインする
        self.client.login(email=email,password=password)

    def test_account_settings(self):
        """アカウント設定画面でアカウントデータが正しく返却されているか確認"""
        response = self.client.post('/account-setting/',{},content_type='application/json')
        user_info = json.loads(response.content)

        #比較用正解JSONデータ
        correct_json_data_account_settings = [
            {
                'user_id': 3,
                'username': 'admin_testuser',
                'default_position': True,
                'is_active': True,
                'is_edit_mode': True
            },
            {
                'user_id': 4,
                'username': 'testuser',
                'default_position': False,
                'is_active': True,
                'is_edit_mode': False
            }
        ]
        self.assertEqual(correct_json_data_account_settings,user_info)

    
class ShiftListCheck(TestCase):
    def setUp(self):
        """テスト用管理ユーザを作成してログイン維持する"""
        shop_id = 0
        username = 'testuser'
        default_position = True
        email = 'test@mail.com'
        password = 'testpassword'
        is_edit_mode = True
        is_active = True
        is_staff = True

        self.user = User.objects.create_user(
            username,
            email,
            password,
            shop_id=shop_id,
            default_position=default_position,
            is_edit_mode=is_edit_mode,
            is_active=is_active,
            is_staff=is_staff
            )

        self.client.login(email=email,password=password)
    
    def test_shift_list(self):
        """シフトをDBに登録してシフトリスト用JSONが正常に返却されるかテスト"""

        #DBにシフトを登録
        post_data_of_shift = {
            "id" : 1,
            "date":"2022-07-01",
            "start":"12:00",
            "end":"18:00", 
        }
        response = self.client.post('/SubmitShift-Ajax/',post_data_of_shift,content_type='application/json')
        self.assertEqual(response.status_code,200)

        post_data_of_shift = {
            "id" : 2,
            "date":"2022-07-02",
            "start":"12:00",
            "end":"15:00", 
        }
        response = self.client.post('/SubmitShift-Ajax/',post_data_of_shift,content_type='application/json')
        self.assertEqual(response.status_code,200)

        post_data_of_shift = {
            "id" : 3,
            "date":"2022-07-02",
            "start":"18:00",
            "end":"22:00", 
        }
        response = self.client.post('/SubmitShift-Ajax/',post_data_of_shift,content_type='application/json')
        self.assertEqual(response.status_code,200)

        post_data_of_shift = {
            "id" : 4,
            "date":"2022-07-30",
            "start":"12:00",
            "end":"18:00", 
        }
        response = self.client.post('/SubmitShift-Ajax/',post_data_of_shift,content_type='application/json')
        self.assertEqual(response.status_code,200)

        post_data_of_shift = {
            "id" : 5
            ,
            "date":"2022-07-31",
            "start":"12:00",
            "end":"18:00", 
        }
        response = self.client.post('/SubmitShift-Ajax/',post_data_of_shift,content_type='application/json')
        self.assertEqual(response.status_code,200)

        #1.シフトリスト(編集済みのシフト)のjsonresponceの中身を確認
        post_data_of_edited_shift_list = {
            "selected_table": True,
            "selected_month": "2022-07-01"
        }
        response = self.client.post('/shift-list-ajax/',post_data_of_edited_shift_list,content_type='application/json')
        self.assertEqual(response.status_code,200)

        content = json.loads(response.content)
        #print(content['shift_lists'][0]['shift_list'])
        res_of_edited_shifts_json = content['shift_lists'][0]['shift_list']

        ##比較用正解JSONデータ
        correct_json_data_edited_shifts = [
            {
                'id': 1,
                'date': '2022-07-01',
                'start': '2022-07-01T03:00:00+00:00',
                'end': '2022-07-01T09:00:00+00:00'
            },
            {
                'id': 2,
                'date': '2022-07-02',
                'start': '2022-07-02T03:00:00+00:00',
                'end': '2022-07-02T06:00:00+00:00'
            },
            {
                'id': 3,
                'date': '2022-07-02',
                'start': '2022-07-02T09:00:00+00:00',
                'end': '2022-07-02T13:00:00+00:00'
            },
            {
                'id': 4,
                'date': '2022-07-30',
                'start': '2022-07-30T03:00:00+00:00',
                'end': '2022-07-30T09:00:00+00:00'
            },
            {
                'id': 5,
                'date': '2022-07-31',
                'start': '2022-07-31T03:00:00+00:00',
                'end': '2022-07-31T09:00:00+00:00'
            }
        ]
        self.assertEqual(correct_json_data_edited_shifts,res_of_edited_shifts_json)

        
        #2. シフトリスト(提出時のシフト)のjsonresponceの中身を確認
        
        ##id=1のシフトをシフト編集画面から削除する
        response = self.client.post('/edit-shift-Ajax/post-shiftdata/delete-shiftdata/',{"id":1},content_type='application/json')
        self.assertEqual(response.status_code,200)

        post_data_of_unedited_shift_list = {
            "selected_table": False,
            "selected_month": "2022-07-01"
        }
        response = self.client.post('/shift-list-ajax/',post_data_of_unedited_shift_list,content_type='application/json')
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        res_of_unedited_shifts_json = content['shift_lists'][0]['shift_list']

        #提出時のシフトは、削除実行しても変化がないことを確認
        self.assertEqual(correct_json_data_edited_shifts,res_of_unedited_shifts_json)