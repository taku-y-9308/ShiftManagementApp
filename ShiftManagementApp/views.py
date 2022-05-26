import json,datetime,secrets,calendar
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
from ShiftManagementApp.models import User,Shift,LINE_USER_ID,Publish_range
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
                if next == None:
                    return HttpResponseRedirect(reverse('ShiftManagementApp:index'))
                else:
                    return HttpResponseRedirect(next)

            else:
                return HttpResponse("アカウントが有効ではありません")
        else:
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
    
    return render(request, 'ShiftManagementApp/login.html')

"""
新規アカウント作成
"""
def create_newaccount(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
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
        end_date = get_last_date(now_JST,1)
    #それ以外のユーザーは来月のみ表示
    else:
        start_date = get_first_date(now_JST,1)
        end_date = get_last_date(now_JST,1)     
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

    if dt.month+target_month < 1:
        return dt.replace(year=dt.year-1,month=12,day=1)
    elif dt.month+target_month > 12:
        return dt.replace(year=dt.year+1,month=1,day=1)
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

    if dt.month+target_month < 1:
        return dt.replace(month=12,day=calendar.monthrange(dt.year-1,12)[1])
    elif dt.month+target_month > 12:
        return dt.replace(month=1,day=calendar.monthrange(dt.year+1,1)[1])
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
シフト締め切り後編集モードの設定画面
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
シフトの送信先
"""
@login_required
def submitshift(request):
    if request.method == 'GET':
        raise Http404()
    print(request.body)
    datas = json.loads(request.body)
    print(datas)
    print(f"startのtype:{type(datas['start'])}")
    start_str = f"{datas['date']}T{datas['start']}"
    start = datetime.datetime.strptime(start_str,'%Y-%m-%dT%H:%M')
    #print(f"start_str:{start_str},start:{start},type(start):{type(start)}")
    end_str = f"{datas['date']}T{datas['end']}"
    end = datetime.datetime.strptime(end_str,'%Y-%m-%dT%H:%M')
    print(request.user.id)
    """
    送信された日付が現在編集可能な場合
    編集可能期間または編集モードのときにシフトを編集できる
    """
    if (Judge_editable(start_str) == True or request.user.is_edit_mode == True):

        '''
        ShiftのidをカレンダーのIDとして渡す
        更新のときはIDを使って更新
        '''
        default_position = User.objects.get(id=request.user.id).default_position
        #idがShiftに存在していたらupdate,id = nullだと存在しないためcreate
        product,created = Shift.objects.update_or_create(
            id = datas['id'],
            defaults = {
                'user':request.user,
                'date':datas['date'],
                'begin':start,
                'finish':end,
                'position': default_position
            }
        )
        print(product.id)

        events = Shift.objects.filter(user=request.user.id)
        response = []
        #create または　updateしたオブジェクトのidを格納
        response.append({
            'res_code':True,
            'shift_id':product.id
        })
        print("編集可能")
        return JsonResponse(response,safe=False)

    #送信された日付が編集可能ではないとき
    else:
        response = []
        response.append({
            'res_code':False
        })
        print("編集不可")
        return JsonResponse(response,safe=False)

'''
シフト提出可能期間かを判定
date_str :YYYY-mm-ddTHH:MM
'''
def Judge_editable(date_str):
    '''
    TimeZone:JST で統一
    '''

    #現在の日本時間出力
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    dt_JST = datetime.datetime.now(JST)
    print(date_str)
    #引数の日付をDate型に変換
    date = datetime.datetime.strptime(date_str+':00+0900','%Y-%m-%dT%H:%M:%S%z')

    # 2022-04-05が与えられたら2022-04-01~2022-04-20に変換
    #すべての時刻をタイムゾーンをJSTにする
    start_date = datetime.datetime(date.year,date.month-1,date.replace(day=1).day,tzinfo=JST)
    end_date = datetime.datetime(date.year,date.month-1,20,tzinfo=JST)
    #与えられた日付が編集可能な時期がを判定
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
    print(json_data)

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
            print(name)
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
        print(user)

        #str→bool型に変換
        if datas['position'] == 'True':
            position = True
        else :
            position = False
        product,created = Shift.objects.update_or_create(
            id = id,
            defaults = {
                'user':user,
                'position': position,
                'date':datas['date'],
                'begin':datas['start'],
                'finish':datas['end']
            }
        )
        print(product)
        print(created)

        return JsonResponse({'':''})

    #staffユーザーではない場合
    else:
        return HttpResponse('アクセス権がありません')

'''
削除リクエストの送信先
'''
@login_required
def editshift_ajax_delete_shiftdata(request):
     #GETリクエストなら404を返す
    if request.method == 'GET':
        raise Http404()
    datas = json.loads(request.body)
    response = []

    #削除リクエストが管理ユーザの場合、無条件で削除実施
    if request.user.is_staff:
        try:
            Shift.objects.get(id=datas['id']).delete()
            response.append({
                'res_code':True
            })
        except Exception as e:
            response.append({
                'res_code':False
            })
            print(e)
        return JsonResponse(response,safe=False)

    #削除リクエストが一般ユーザーの場合、編集可能期間かどうかで可否を変える
    else:
        """
        削除リクエストの判定
        編集可能期間もしくは、編集モードの時に削除リクエストを受け付ける
        """
        if (Judge_editable(datas['start']) == True or request.user.is_edit_mode == True):
            #getは対象が存在しないと例外を返すため念の為try文にしている
            try:
                Shift.objects.get(id=datas['id']).delete()
                response.append({
                    'res_code':True
                })
            except Exception as e:
                print(e)
        else:
            response.append({
                'res_code':False
            })
        return JsonResponse(response,safe=False)

"""
シフトの公開設定
"""
@login_required
def edit_shift_publish_shift(request):
    if request.method == 'GET':
        raise Http404()
    if request.user.is_staff:
        publish_range = json.loads(request.body)
        publish_start = publish_range['publish_shift_start']

        #タイムゾーンの関係でカレンダーのendが１日少なく表示されてしまうため+1する
        publish_end = datetime.datetime.strptime( publish_range['publish_shift_end'],'%Y-%m-%d') + datetime.timedelta(days=1)

        #公開範囲のShiftのpublishをTrueにする
        Shift.objects.filter(date__gte=publish_start,date__lte=publish_end).update(publish=True)

        Publish_range.objects.update_or_create(
            id=1,
            defaults={
                'Publish_shift_start':publish_start,
                'Publish_shift_end':publish_end

            }
        )
    response = {}
    return JsonResponse(response)
    
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
    template_name = 'ShiftManagementApp/password_reset_form.html'
    success_url = reverse_lazy('ShiftManagementApp:password_reset_done')

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'ShiftManagementApp/password_reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'ShiftManagementApp/password_reset_confirm.html'
    success_url = reverse_lazy('ShiftManagementApp:password_reset_complete')

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'ShiftManagementApp/password_reset_complete.html'