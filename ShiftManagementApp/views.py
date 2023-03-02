from cmath import log
import json,datetime,secrets,calendar,logging,pytz
from sre_constants import SUCCESS
import re
from asyncio import events
from curses import reset_prog_mode
from email.policy import default
from pickletools import read_unicodestring8
from re import A, template
from this import d
from tracemalloc import start
from urllib import response
from xmlrpc.client import boolean
from django.views import generic
from ShiftManagementApp.models import User,Shift,Shift_Archive,LINE_USER_ID,Publish_range,Deadline
from ShiftManagementApp.form import SubmitShift,SignUpForm,CreateAccount,ContactForm
from django.urls import reverse,reverse_lazy
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import Http404
from django.core.mail import EmailMultiAlternatives

"""
ログレベルセット
"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

"""
ログイン
"""
def Login(request):
    if request.method == 'POST':
        EMAIL = request.POST.get('email')
        PASS = request.POST.get('password')
        try:
            next = request.POST.get('next')
        except :
            next = None
        user = authenticate(email=EMAIL, password=PASS)

        if user:
            if user.is_active:
                login(request,user)
                print(f'[INFO]ログイン成功しました。userid:{request.user.id}')
                if next == None:
                    return HttpResponseRedirect(reverse('ShiftManagementApp:index'))
                else:
                    return HttpResponseRedirect(next)

            else:
                error_message = "アカウントが有効化されていません。"
                params = {
                    "error_message":error_message
                }
                return render(request,'ShiftManagementApp/login.html',params)
        else:
            print(f'[INFO]ログイン失敗しました。 userid:{request.user.id}')
            error_message = "ログインIDまたはパスワードが違います"
            params = {
                "error_message":error_message
            }
            return render(request,'ShiftManagementApp/login.html',params)
    # リクエストがGETだった場合
    else:
        next = request.GET.get('next')
        params = {
            "next":next
        }
        return render(request, 'ShiftManagementApp/login.html',params)

"""
ログアウト
"""
@login_required
def Logout(request):
    logout(request)
    print(f'[INFO]ログアウトしました。userid:{request.user.id}')
    return render(request, 'ShiftManagementApp/login.html')

"""
新規アカウント作成
"""
def create_newaccount(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            print(f'[INFO]新規アカウントが作成されました。userid:{request.user.id}')
            return HttpResponseRedirect(reverse('ShiftManagementApp:Login'))
    #GETリクエスト時(通常のアクセス時) 
    else:
        form = SignUpForm()
    return render(request,'ShiftManagementApp/create_account.html',{'form': form})

"""
ホーム
"""
@login_required
def home(request):

    #PWAとして使用しているユーザーを特定する
    pwa_user = request.GET.get('pwa')

    if pwa_user is None:
        pass
    elif pwa_user == '1':
        User.objects.filter(id=request.user.id).update(is_pwa_user=True)

    arr2 = []
    shifts = Shift.objects.filter(user=request.user.id)
    for shift in shifts:
        arr = {
            'id':shift.id,
            'titie':'TEST',
            'start':shift.begin,
            'end':shift.finish,
            'backgroundColor': "red",
		    'borderColor': "red",
		    'editable': 'true'
        }
        arr2.append(arr)
    
    #カレンダーの表示範囲を公開設定されている範囲のみ表示する
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now_JST = datetime.datetime.now(JST)
    now_JST_str = now_JST.strftime('%Y-%m-%dT%H:%M') #YYYY-MM-ddTHH:mm形式の文字列に変換

    start_date = get_first_date(now_JST,-1)
    try:
        end_date = Publish_range.objects.get(id=1).Publish_shift_end
    except:
        end_date = get_last_date(now_JST,1)

    params = {
        'shift':arr2,
        'User':request.user,
        'start_date':start_date.strftime('%Y-%m-%d'),
        'end_date':end_date.strftime('%Y-%m-%d')
    }
    return render(request,'ShiftManagementApp/index.html',context=params)

"""
シフト提出画面
"""
@login_required
def submit_shift(request):
    arr2 = []
    shifts = Shift.objects.filter(user=request.user.id)
    for shift in shifts:
        arr = {
            'id':shift.id,
            'titie':'TEST',
            'start':shift.begin,
            'end':shift.finish,
            'backgroundColor': "red",
		    'borderColor': "red",
		    'editable': 'true'
        }
        arr2.append(arr)

    #カレンダーの表示範囲を設定
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now_JST = datetime.datetime.now(JST)

    #編集モードがTrueのユーザーは今月と来月を表示
    if request.user.is_edit_mode:
        start_date = get_first_date(now_JST,0)
        end_date = get_last_date(now_JST,1) + datetime.timedelta(days=1) #FullCalendarはUTCで認識されてしまうため
    #それ以外のユーザーは来月のみ表示
    else:
        start_date = get_first_date(now_JST,1)
        end_date = get_last_date(now_JST,1) + datetime.timedelta(days=1) #FullCalendarはUTCで認識されてしまうため
    print(f"start_date:{start_date}")
    print(f"end_date:{end_date}")
    params = {
        'shift':arr2,
        'User':request.user,
        'start_date':start_date.strftime('%Y-%m-%d'),
        'end_date':end_date.strftime('%Y-%m-%d')
    }
    return render(request,'ShiftManagementApp/submit_shift.html',context=params)

"""
指定した月の月初めdatetimeオブジェクトを返す
引数
dt:
date,datetimeオブジェクト

target_month:
defalut=0
-1:前月
0:当月
1:来月

返り値:指定のtargetmonthの月初めdatetimeオブジェクト
"""

def get_first_date(dt,target_month=0):
    if not -1 <= target_month <= 1:
        raise ValueError("target_monthは-1~1の範囲である必要があります")
    
    if dt.month == 1:
        if target_month == -1:
            return datetime.date(dt.year-1,12,1)
        elif target_month == 0:
            return datetime.date(dt.year,1,1)
        elif target_month == 1:
            return datetime.date(dt.year,2,1)
        else:
            pass
    elif dt.month == 12:
        if target_month == -1:
            return datetime.date(dt.year,11,1)
        elif target_month == 0:
            return datetime.date(dt.year,12,1)
        elif target_month == 1:
            return datetime.date(dt.year+1,1,1)
        else:
            pass
    else:
        return dt.replace(month=dt.month+target_month,day=1)

"""
指定した月の月末datetimeオブジェクトを返す
引数
dt:
date,datetimeオブジェクト

target_month:
defalut=0
-1:前月
0:当月
1:来月

返り値:指定のtargetmonthの月末datetimeオブジェクト
"""
def get_last_date(dt,target_month=0):
    if not -1 <= target_month <= 1:
        raise ValueError("target_monthは-1~1の範囲である必要があります")

    if dt.month == 1:
        if target_month == -1:
            return datetime.date(dt.year-1,12,31)
        elif target_month == 0:
            return datetime.date(dt.year,1,31)
        elif target_month == 1:
            return dt.replace(month=2,day=calendar.monthrange(dt.year,2)[1])
        else:
            pass
    elif dt.month == 12:
        if target_month == -1:
            return datetime.date(dt.year,11,30)
        elif target_month == 0:
            return datetime.date(dt.year,12,31)
        elif target_month == 1:
            return datetime.date(dt.year+1,1,31)
        else:
            pass
    else:
        return dt.replace(month=dt.month+target_month,day=calendar.monthrange(dt.year,dt.month+target_month)[1])

"""
お問い合わせフォーム
"""
@login_required
def contact(request):
    if request.method == 'GET':
        form = ContactForm()
        params = {
            'form':form,
            'user_id':request.user.id
        }
        return render(request,"ShiftManagementApp/contact.html",params)
    else:
        form_raw = ContactForm(request.POST) #ユーザーID:1で送信されたformデータ（デフォルトで1になるようにしている）
        #バリデーションに問題がない時
        if form_raw.is_valid():
            form = form_raw.save(commit=False)
            form.user = request.user #本来のユーザーIDで書き換える
            form.save()

            '''
            メール送信（フォーム送信者用）
            '''
            subject = 'お問い合わせありがとうございます'
            text_content = 'シフト管理アプリをご利用いただきましてありがとうございます。'\
                'お問い合わせ受け付けました。'\
                '管理者から登録のメールアドレス宛に返信いたします。'
            html_content = 'シフト管理アプリをご利用いただきましてありがとうございます。<br>'\
                'お問い合わせ受け付けました。<br>'\
                '管理者から登録のメールアドレス宛に返信いたします。<br>'\
        
            from_email = 'no-reply@shiftmanagementapp.com'
            to_email = request.user.email

            send_email(subject,text_content,html_content,from_email,to_email)

            '''
            メール送信（管理者用）
            '''
            subject = '新規のお問い合わせを受け付けました'
            text_content = f'新規のお問い合わせがありました。'\
                f'【ShopID】:{request.user.shop_id} '\
                f'【Email】:{request.user.email} '\
                f'【ユーザー名】:{request.user.username} '\
                f'【タイトル】：{form.title} '\
                f'【内容】：{form.text} '\
                '確認はこちらからお願いします。'\
                'http://shiftmanagementapp.com/admin'
            html_content = f'新規のお問い合わせがありました。<br>'\
                f'【ShopID】:{request.user.shop_id} <br>'\
                f'【Email】:{request.user.email} <br>'\
                f'【ユーザー名】:{request.user.username} <br><br>'\
                f'【タイトル】：{form.title} <br>'\
                f'【内容】：{form.text} <br>'\
                '確認はこちらからお願いします。<br>'\
                '<a href="http://shiftmanagementapp.com/admin">http://shiftmanagementapp.com/admin</a>'
        
            from_email = 'no-reply@shiftmanagementapp.com'
            to_email = 'y.takumi4@gmail.com'

            send_email(subject,text_content,html_content,from_email,to_email)

            return HttpResponseRedirect(reverse('ShiftManagementApp:contact_success'))
        
        #お問い合わせフォームに不備があった時
        else:
            return render(request,"ShiftManagementApp/contact.html",{'form':form})

"""
お問い合わせフォーム送信完了画面
"""
@login_required
def contact_success(request):
    return render(request,'ShiftManagementApp/contact_success.html')

"""
【未使用】シフト締め切り後編集モードの設定画面
"""
@login_required
def edit_shift_mode(request):
    if request.user.is_staff:
        if request.method == 'GET':
            list_of_users = list(User.objects.filter(shop_id=request.user.shop_id))
            params = {
                'list_of_users':list_of_users
            }
            
        else:
            user_id = request.POST.get('user_id')
            if user_id != 'test':
                if User.objects.get(id=user_id).is_edit_mode:
                    print(type(User.objects.get(id=user_id).is_edit_mode))
                    User.objects.filter(id=user_id).update(is_edit_mode=False)
                else:
                    User.objects.filter(id=user_id).update(is_edit_mode=True)

            list_of_users = list(User.objects.filter(shop_id=request.user.shop_id))
            params = {
                'list_of_users':list_of_users
            }

        return render(request,'ShiftManagementApp/edit_shift_mode.html',params)
    else:
        return HttpResponse('アクセス権がありません')
"""
通常のシフト送信先
"""
@login_required
def submitshift(request):
    if request.method == 'GET':
        raise Http404()
    datas = json.loads(request.body)
    print(f"[INFO]シフトが送信されました。userid:{request.user.id} body:{datas}")
    start_str = f"{datas['date']}T{datas['start']}"
    start = datetime.datetime.strptime(start_str,'%Y-%m-%dT%H:%M')
    #print(f"start_str:{start_str},start:{start},type(start):{type(start)}")
    end_str = f"{datas['date']}T{datas['end']}"
    end = datetime.datetime.strptime(end_str,'%Y-%m-%dT%H:%M')


    # バリデーション
    if start > end:
        response = HttpResponse()
        message = '終了時刻は開始時刻より後ろである必要があります'
        response.status_code = 400
        response.content = message
        return response
    
    """
    編集可能期間または編集モードのときにシフトを編集できる
    """
    if (Judge_editable(request.user.shop_id,start_str) == True or request.user.is_edit_mode == True):
        print("[INFO]編集可能なシフトです")

        '''
        ShiftのidをカレンダーのIDとして渡す
        更新のときはIDを使って更新
        '''
        default_position = User.objects.get(id=request.user.id).default_position
        
        #idがShiftに存在していたらupdate,id = nullだと存在しないためcreate
        
        #DBの成功数をカウントする
        success_count = 0
        #メインDBテーブルに書き込む
        try:
            product_of_main_table,created_of_main_table = Shift.objects.update_or_create(
                id = datas['id'],
                defaults = {
                    'user':request.user,
                    'date':datas['date'],
                    'begin':start,
                    'finish':end,
                    'position': default_position
                }
            )
            print(f"[INFO]メインテーブルの更新が正常に完了しました。product_of_main_table.id:{product_of_main_table.id}")
            success_count +=1
        except Exception as e:
            print(f"[ERROR]メインテーブルの更新が失敗しました。product_of_main_table.id:{product_of_main_table.id} reason:{e}")
            

        #アーカイブテーブルに書き込む
        #プライマリーキーには、メインテーブルと同一の物を使用する
        """
        #クライアントからid=Noneで送信されたら、新規シフト判定
        if datas['id'] is None:
            primary_key = None
        else:
            primary_key = product_of_main_table.id
        """

        try:
            product_of_archive_table,created_of_archive_table = Shift_Archive.objects.update_or_create(
            id = product_of_main_table.id,
            defaults = {
                    'user':request.user,
                    'date':datas['date'],
                    'begin':start,
                    'finish':end,
                    'position': default_position
                }
            )
            print(f"[INFO]アーカイブテーブルの更新が正常に完了しました。product_of_archive_table.id:{product_of_archive_table.id}")
            success_count +=1
        except Exception as e:
            print(f"[ERROR]アーカイブテーブルの更新に失敗しました。product_of_archive_table.id:{product_of_archive_table.id} reason:{e}")

        events = Shift.objects.filter(user=request.user.id)
        response = []
        
        #shift_idにはcreate または　updateしたオブジェクトのidを格納
        #両テーブルの更新に成功した時
        if success_count == 2:
            response.append({
                'res_code':True,
                'shift_id':product_of_main_table.id
            })
        #どちらかのテーブル、または両テーブルの更新に失敗した場合
        else:
            response.append({
                'res_code': False,
                'error_code': 1,
                'shift_id':product_of_main_table.id
            })
        return JsonResponse(response,safe=False)

    #送信された日付が編集可能ではないとき
    else:
        response = []
        response.append({
            'res_code':False,
            'error_code': 2
        })
        print("[INFO]編集可能でないシフトです")
        return JsonResponse(response,safe=False)


'''
所属するshop_idと判定したい日付を入れると、シフト提出可能期間かを判定
date_str :YYYY-mm-ddTHH:MM
shop_id: 1
'''
def Judge_editable(shop_id,date_str):
    '''
    TimeZone:JST で統一
    '''

    #現在の日本時間出力
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    dt_JST = datetime.datetime.now(JST)
    #print(date_str)
    #引数の日付をDate型に変換
    date = datetime.datetime.strptime(date_str+':00+0900','%Y-%m-%dT%H:%M:%S%z')

    #shop_idから締切日を判定する
    #締切日未設定のshopの場合はデフォルトの20日をセットする
    deadline, created = Deadline.objects.get_or_create(
        shop_id = shop_id,
        defaults = {
            'deadline': 20
        }
    )

    # シフト提出可能日を算出する
    # deadlineが20の場合、2022-04-05が与えられたら2022-03-01~2022-03-20が提出可能日になる
    if date.month == 1:
        start_date = datetime.datetime(date.year-1,12,date.replace(day=1).day,tzinfo=JST)
        end_date = datetime.datetime(date.year-1,12,deadline.deadline,tzinfo=JST)
    else:
        start_date = datetime.datetime(date.year,date.month-1,date.replace(day=1).day,tzinfo=JST)
        end_date = datetime.datetime(date.year,date.month-1,deadline.deadline,tzinfo=JST)

    if start_date<dt_JST<end_date:
        return True
    else:
        return False

'''
シフト編集画面のトップページ表示
'''
@login_required
def editshift(request):

    members = User.objects.filter(shop_id=request.user.shop_id)
    user = request.user
    params = {
        'members':members,
        'User':user
    }
    return render(request,'ShiftManagementApp/editshift.html',params)


'''
【シフト編集画面】
シフト編集画面の日付を入力したときの送信先
シフト編集画面描画用のシフトデータをjsonで返す
'''
@login_required
def editshift_ajax(request):
    #GETリクエストなら404を返す
    if request.method == 'GET':
        raise Http404()

    json_data = json.loads(request.body)
    date = json_data['date']
    #print(json_data)

    arr2 = []
    
    #該当のシフトを取得(User.idの昇順で並び替える),管理者かそうでないかで取得するシフトを変える
    if request.user.is_staff:
        shifts = Shift.objects.select_related('user').filter(date=date).order_by('user__id')
    else:
        shifts = Shift.objects.select_related('user').filter(date=date,publish=True).order_by('user__id')
    
    for shift in shifts:
        #管理ユーザーと同じshop_idのシフトのみ表示（他店のシフトは表示しない）
        if shift.user.shop_id == request.user.shop_id:
            name = User.objects.get(id=shift.user.id).username
            #print(name)
            #positionによってバーに適用する色を変える
            position = shift.position
            if position == True:
                style = '#0000ff' #blue
            else:
                style = '#ff0000' #red
            arr = {
                'shift_id':shift.id,
                'name':name,
                'date':shift.date,
                'style':style,
                'start':shift.begin,
                'end':shift.finish,
            }
            arr2.append(arr)
    return JsonResponse(arr2,safe=False)



'''
【管理者のみ】
【シフト編集画面】
シフトデータを新規追加or編集したときの送信先
'''
@login_required
def editshift_ajax_post_shiftdata(request):
    #GETリクエストなら404を返す
    if request.method == 'GET':
        raise Http404()

    #スタッフユーザー(管理ユーザー)のみ実行可 
    if request.user.is_staff:
        datas = json.loads(request.body)
        id = datas['id']

        #更新のときはmemberはNoneで送信
        if datas['member'] is None:
            user = Shift.objects.get(id=id).user
        #新規作成のときはmemberにuserをPKから参照
        else:
            user = User.objects.get(id=datas['member'])
        #print(user)

        #str→bool型に変換
        if datas['position'] == 'True':
            position = True
        else :
            position = False

        #送信されたシフトが公開済みシフトの場合はPublish＝Trueにする
        publish_range = Publish_range.objects.get(id=1)
        publish_shift_start_native = datetime.datetime.combine(publish_range.Publish_shift_start,datetime.time())
        publish_shift_end_native = datetime.datetime.combine(publish_range.Publish_shift_end,datetime.time())

        #timezoneありに変換
        publish_shift_start = pytz.timezone('Asia/Tokyo').localize(publish_shift_start_native)
        publish_shift_end = pytz.timezone('Asia/Tokyo').localize(publish_shift_end_native)

        if publish_shift_start <= datetime.datetime.strptime(datas['date']+"T00:00:00+0900",'%Y-%m-%dT%H:%M:%S%z') <= publish_shift_end:
            print("[INFO]公開済み範囲のシフトが送信されました")
            is_publish = True
        else:
            print("[INFO]公開済み範囲外のシフトが送信されました")
            is_publish = False

        try:
            product,created = Shift.objects.update_or_create(
                id = id,
                defaults = {
                    'user':user,
                    'position': position,
                    'date':datas['date'],
                    'begin':datas['start'],
                    'finish':datas['end'],
                    'publish':is_publish
                }
            )
            print(f'[INFO]DBへの登録に成功しました product.id:{product.id}')
            res_code = True
        except Exception as e:
            print(f'[ERROR]DBへの登録に失敗しました product.id:{product.id} reason:{e}')
            res_code = False

        return JsonResponse({'res_code':res_code})

    #staffユーザーではない場合
    else:
        print(f'[INFO]staffユーザーではないユーザーがシフト編集画面にアクセスしました。user_id:{request.user.id}')
        return HttpResponse('アクセス権がありません')

'''
個人画面からの削除リクエストの送信先
メインテーブルとアーカイブテーブルから削除する
'''
@login_required
def editshift_ajax_delete(request):
     #GETリクエストなら404を返す
    if request.method == 'GET':
        raise Http404()
    datas = json.loads(request.body)
    delete_shift_id = datas['id']
    response = []

    """
    削除リクエストの判定
    編集可能期間もしくは、編集モードの時に削除リクエストを受け付ける
    """
    for_judge_date = f"{datas['date']}T{datas['start']}"
    if (Judge_editable(request.user.shop_id,for_judge_date) == True or request.user.is_edit_mode == True):
        #getは対象が存在しないと例外を返すため念の為try文にしている
        
        #メインテーブルから削除
        try:
            Shift.objects.get(id=datas['id']).delete()
            response.append({
                'res_code':True
            })
            print(f'[INFO]メインテーブルのシフトが削除されました。 delete_shift_id:{delete_shift_id}')
        except Exception as e:
            print(f'[ERROR]メインテーブルのシフト削除に失敗しました。 reason:{e}')
        
        #アーカイブテーブルから削除
        try:
            Shift_Archive.objects.get(id=datas['id']).delete()
            print(f'[INFO]アーカイブテーブルのシフトが削除されました。 delete_shift_id:{delete_shift_id}')
        except Exception as e:
            print(f'[ERROR]アーカイブテーブルのシフト削除に失敗しました。 reason:{e}')
    else:
        response.append({
            'res_code':False
        })
        print(f'[INFO]編集可能期間外もしくは、編集モードでないためシフトを削除できませんでした. delete_shift_id:{delete_shift_id}')
    return JsonResponse(response,safe=False)

"""
【管理者のみ】
【シフト編集画面】
シフト編集画面からの削除リクエスト
メインテーブルのみ削除する
"""
def editshift_ajax_delete_shiftdata(request):
    if request.user.is_staff:
        if request.method == 'GET':
            raise Http404()

        datas = json.loads(request.body)
        delete_shift_id = datas['id']
        response = []

        #メインテーブルのみ削除
        try:
            Shift.objects.get(id=datas['id']).delete()
            response.append({
                'res_code':True
            })
            print(f'[INFO]シフトが削除されました。 delete_shift_id:{delete_shift_id}')
        except Exception as e:
            response.append({
                'res_code':False
            })
            print(f'[ERROR]シフト削除に失敗しました。 reason:{e}')
        return JsonResponse(response,safe=False)
        
    else:
        print(f'[INFO]staffユーザーではないユーザーがシフト編集画面にアクセスしました。user_id:{request.user.id}')
        return HttpResponse('アクセス権がありません')


"""
シフトの公開設定
"""
@login_required
def edit_shift_publish_shift(request):
    if request.method == 'GET':
        raise Http404()
    if request.user.is_staff:
        try:
            publish_range = json.loads(request.body)
            publish_start = publish_range['publish_shift_start']

            #タイムゾーンの関係でカレンダーのendが１日少なく表示されてしまうため+1する
            publish_end = datetime.datetime.strptime( publish_range['publish_shift_end'],'%Y-%m-%d') + datetime.timedelta(days=1)

            #公開範囲のShiftのpublishをTrueにする
            Shift.objects.select_related('user').filter(date__gte=publish_start,date__lte=publish_end,user__shop_id=request.user.shop_id).update(publish=True)

            Publish_range.objects.update_or_create(
                id=1,
                defaults={
                    'Publish_shift_start':publish_start,
                    'Publish_shift_end':publish_end

                }
            )
            
            #is_edit_modeがTrueになっているユーザーをFalseに変える
            User.objects.filter(shop_id=request.user.shop_id,is_edit_mode=True).update(is_edit_mode=False)
            print(f'[INFO]シフト公開範囲が設定されました。 終了日は-1日してください。 {publish_start}~{publish_end}')
            res_code = True
        except Exception as e:
            print(f'[ERROR]シフト公開範囲の設定に失敗しました。 {publish_start}~{publish_end} reason:{e}')
            res_code = False

    else:
        res_code = False
        print(f'staffユーザーではないユーザーによるアクセスがありました。 user_id:{request.user.id}')

    response = {'res_code':res_code}
    return JsonResponse(response)


"""
シフト一覧表表示用
"""
@login_required
def shift_list(request):
    if request.user.is_staff:
        now = datetime.datetime.now()
        this_month = datetime.date(now.year,now.month,1)

        # 1月と12月は別処理にする
        if now.month == 1:
            last_month = datetime.date(now.year-1,12,1)
            next_month = datetime.date(now.year,now.month+1,1)
        elif now.month == 12:
            last_month = datetime.date(now.year,now.month-1,1)
            next_month = datetime.date(now.year+1,1,1)
        else:
            last_month = datetime.date(now.year,now.month-1,1)
            next_month = datetime.date(now.year,now.month+1,1)

        params= {
            'last_month_for_value': last_month.strftime('%Y-%m-%d'),
            'this_month_for_value': this_month.strftime('%Y-%m-%d'),
            'next_month_for_value': next_month.strftime('%Y-%m-%d'),
            'last_month_for_display': last_month.strftime('%Y-%m'),
            'this_month_for_display': this_month.strftime('%Y-%m'),
            'next_month_for_display': next_month.strftime('%Y-%m')
        }
        return render(request,'ShiftManagementApp/shift_list.html',params)
    else:
        print(f'staffユーザーではないユーザーによるアクセスがありました。 user_id:{request.user.id}')
        return HttpResponse('アクセス権がありません')


"""
特定期間、かつ同じshop_idのシフトをすべてJSONで返す
"""
@login_required
def shift_list_ajax(request):
    if request.user.is_staff:
        json_total_shift_stored = {} #全体のシフトが格納されたjson
        tmp_arr2 = []

        res = json.loads(request.body)
        #print(res["selected_month"])

        #編集済みのシフト:True,提出時のシフト:False
        type_of_shift_table = res['selected_table']
        """
        if res['selected_table'] == 'true':
            type_of_shift_table = True
        elif res['selected_table'] == 'false':
            type_of_shift_table = False
        else:
            type_of_shift_table = None

        """

        dt = datetime.datetime.strptime(res["selected_month"],'%Y-%m-%d')
        selected_month_beginning = dt

        if dt.month == 12:
            selected_month_end = datetime.date(dt.year+1,1,1) - datetime.timedelta(days=1)
        else:
            selected_month_end = datetime.date(dt.year,dt.month+1,1) - datetime.timedelta(days=1)

        selected_month_beginning_str = selected_month_beginning.strftime('%Y-%m-%d')
        selected_month_end_str = selected_month_end.strftime('%Y-%m-%d')


        users= User.objects.filter(shop_id=request.user.shop_id)
        #すべてのユーザーのシフトをjson_total_shift_storedに格納する
        for user in users:
            shift_list_each_private = {} #個人ごとのシフトリストを格納
            tmp_arr = []
            
            """
            dateオブジェクトでも文字列でもいけるが、どっちにする？
            タイムゾーン考慮する
            """
            """
            選択されたshift_tableのタイプ(編集済みのシフトと提出時のシフト)によって取得するシフトを変える
            """
            if type_of_shift_table:
                shifts = list(Shift.objects.filter(user=user,date__gte=selected_month_beginning,date__lte=selected_month_end).order_by('date'))
            elif type_of_shift_table == False:
                shifts = list(Shift_Archive.objects.filter(user=user,date__gte=selected_month_beginning,date__lte=selected_month_end).order_by('date'))
            else:
                pass

            print(f'[INFO]selected_month_beginning:{selected_month_beginning_str} selected_month_end:{selected_month_end_str}')
            shift_list_each_private['username'] = user.username

            #特定個人のシフトをすべてshift_list_indivisualに格納する
            for shift in shifts:
                tmp_arr.append({
                    "id": shift.id,
                    "date": shift.date.isoformat(),
                    "start": shift.begin.isoformat(),
                    "end": shift.finish.isoformat()   
                })
            shift_list_each_private['shift_list'] = tmp_arr
            tmp_arr2.append(shift_list_each_private)

        
        json_total_shift_stored['shift_lists'] = tmp_arr2

        return JsonResponse(json_total_shift_stored)
    else:
        print(f'staffユーザーではないユーザーによるアクセスがありました。 user_id:{request.user.id}')
        return HttpResponse('アクセス権がありません')

"""
印刷用ページ作成
"""
@login_required
def shift_list_print(request):
    if request.user.is_staff:
        now = datetime.datetime.now()
        last_month = datetime.date(now.year,now.month-1,1)
        this_month = datetime.date(now.year,now.month,1)
        next_month = datetime.date(now.year,now.month+1,1)
        params= {
            'last_month_for_value': last_month.strftime('%Y-%m-%d'),
            'this_month_for_value': this_month.strftime('%Y-%m-%d'),
            'next_month_for_value': next_month.strftime('%Y-%m-%d'),
            'last_month_for_display': last_month.strftime('%Y-%m'),
            'this_month_for_display': this_month.strftime('%Y-%m'),
            'next_month_for_display': next_month.strftime('%Y-%m')
        }
        return render(request,'ShiftManagementApp/shift_list_print.html',params)
    else:
        print(f'staffユーザーではないユーザーによるアクセスがありました。 user_id:{request.user.id}')
        return HttpResponse('アクセス権がありません')

"""
設定画面
"""
@login_required
def general_settings(request):
    if request.method == 'GET':
        return render(request,'ShiftManagementApp/general_settings.html')
    else:
        posted_data = json.loads(request.body)
        res_data = {}
        
        #設定画面が読み込まれた時に返す
        if posted_data['post_data_type'] == None:
            if request.user.is_staff:
                user = User.objects.filter(id=request.user.id)[0]
                deadline, created = Deadline.objects.get_or_create(
                    shop_id = user.shop_id,
                    defaults = {
                        'deadline': 20
                    }
                )
                res_data = {
                    'shop_id': user.shop_id,
                    'username': user.username,
                    'email': user.email,
                    'deadline': deadline.deadline
                }
            else:
                user = User.objects.filter(id=request.user.id)[0]
                res_data = {
                    'shop_id': user.shop_id,
                    'username': user.username,
                    'email': user.email
                }
            res_data['res_code'] = 0
        elif posted_data['post_data_type'] == 'modified_username':
            try:
                User.objects.filter(id=request.user.id).update(username=posted_data['modified_username'])
                res_code=0
            except:
                res_code=1
            res_data['res_code'] = res_code
        elif posted_data['post_data_type'] == 'modified_email':
            try:
                User.objects.filter(id=request.user.id).update(email=posted_data['modified_email'])
                res_code=0
            except:
                res_code=1
            res_data['res_code'] = res_code
        elif posted_data['post_data_type'] == 'modified_deadline':
            try:
                Deadline.objects.filter(shop_id=request.user.shop_id).update(deadline=posted_data['modified_deadline'])
                res_code=0
            except:
                res_code=1
            res_data['res_code'] = res_code   
    return JsonResponse(res_data)
            


"""
アカウント設定画面
"""
@login_required
def account_setting(request):
    if request.method == 'GET':
        return render(request,'ShiftManagementApp/account_settings.html')
    
    #POSTリクエストで実行
    else :
        #スタッフユーザーのみ実行可能        
        if request.user.is_staff:
            users = User.objects.filter(shop_id=request.user.shop_id).order_by('id')
            user_list_private = {} #個人ごとのユーザーリストを格納
            user_list = [] # return用の完全なユーザーリストを格納
            for user in users:
                user_list_private = {
                    "user_id": user.id,
                    "username": user.username,
                    "default_position": user.default_position,
                    "is_active": user.is_active,
                    "is_edit_mode": user.is_edit_mode
                }
                user_list.append(user_list_private)
            return JsonResponse(user_list,safe=False)
            
        #一般ユーザーの場合
        else:
            print(f'staffユーザーではないユーザーによるアクセスがありました。 user_id:{request.user.id}')
            return JsonResponse({"error_mes":"アクセス権限がありません"})

"""
指定カラムのbool値を変更する
または
特定ユーザーを削除する
"""
@login_required
def valid_invalid_change(request):
    if request.method == 'POST':
        if request.user.is_staff:
            res = json.loads(request.body)
            user_id = res['user_id']
            target = res['target']
            current_bool =  bool(res['current_bool'])
            if target == 'is_active':
                user = User.objects.filter(id=user_id).update(is_active=(not current_bool))
                print(f'[INFO]ユーザーのis_activeが変更されました。userid:{user_id} {current_bool}→{not current_bool}')
            elif target == 'is_edit_mode':
                user = User.objects.filter(id=user_id).update(is_edit_mode=(not current_bool))
                print(f'[INFO]ユーザーのis_edit_modeが変更されました。userid:{user_id} {current_bool}→{not current_bool}')
            elif target == 'is_delete':
                user = User.objects.filter(id=user_id).delete()
                print(f'[INFO]ユーザーが削除されました。userid:{user_id}')
            else:
                print(f'[INFO]指定の値ではないtargetが送信されました userid:{user_id}')
                return JsonResponse({"error_mes":"targetが指定の値ではありません"})
            
            return JsonResponse({"status_code":0})
    else:
        print(f'staffユーザーではないユーザーによるアクセスがありました。 user_id:{request.user.id}')
        raise Http404()



"""
メール送信用
"""
def send_email(subject,text_content,html_content,from_email,to_emails):
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_emails])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

"""
LINEアカウント連携表示用
"""
@login_required
def line(request):
    return render(request,'ShiftManagementApp/line.html')

"""
LINEアカウント連携
"""
@login_required
def account_linkage(request):
    linkToken = request.GET.get('linkToken')
    User = request.user
    nonce = secrets.token_urlsafe(32)
    LINE_USER_ID.objects.update_or_create(
        user = User, #Userインスタンス自身を渡す
        defaults = {
            'nonce': nonce
        }
    )

    return  HttpResponseRedirect(f'https://access.line.me/dialog/bot/accountLink?linkToken={linkToken}&nonce={nonce}')

"""
パスワードリセット
"""
class PasswordReset(PasswordResetView):
    email_template_name = "ShiftManagementApp/password_reset_email.html"
    template_name = 'ShiftManagementApp/password_reset_form.html'
    success_url = reverse_lazy('ShiftManagementApp:password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'ShiftManagementApp/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'ShiftManagementApp/password_reset_confirm.html'
    success_url = reverse_lazy('ShiftManagementApp:password_reset_complete')

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'ShiftManagementApp/password_reset_complete.html'