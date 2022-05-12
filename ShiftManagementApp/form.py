#from tkinter import Widget
from django.forms import ModelForm,Textarea
from django import forms
from ShiftManagementApp.models import Shift,User,Contact
from django.contrib.auth.forms import UserCreationForm

class SubmitShift(ModelForm):
    class Meta:
        model = Shift
        fields = ('user','date','begin','finish')

class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ('user','title','text')
        '''
        contactフォームを送信するときに無条件でユーザーID:1で送信する
        ユーザーIDに何も入ってないと、不完全な状態であるためform.save(commit=False)がエラーを吐く
        userはhiddenタグで非表示にしている
        '''
        widgets = {
            'user':forms.NumberInput(attrs={
                'class': 'form-control',
                'type':'hidden',
                'value':1
                }),
            'title':forms.TextInput(attrs={'class': 'form-control'}),
            'text':Textarea(attrs={'class': 'form-control'})
        }

class CreateAccount(forms.Form):

    email = forms.EmailField(label='メールアドレス',widget=forms.TextInput(attrs={
        'placeholder':'example@mail.com',
        'class':'form-control'
        }))

    password1 = forms.CharField(label='パスワード' ,widget=forms.PasswordInput(), min_length=8)
    password2 = forms.CharField(label='パスワード' ,widget=forms.PasswordInput(), min_length=8)

    shop_id = forms.IntegerField(label='ショップコード',widget=forms.NumberInput(attrs={
        'placeholder':1,
         'class':'form-control'
        }))
    username = forms.CharField(label='姓',widget=forms.TextInput(attrs={
        'placeholder':'山田',
        'class':'form-control'
        }))
    
    positions = [
        ('キッチン',False),
        ('ホール',True)
    ]
    position = forms.ChoiceField(label='ポジション',choices=positions,widget=forms.Select(attrs={
        'class':'form-control'
    }))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='メールアドレス',widget=forms.TextInput(attrs={
        'placeholder':'example@mail.com',
        'class':'form-control'
        }))
    password1 = forms.CharField(label='パスワード' ,widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    password2 = forms.CharField(label='パスワード' ,widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))
    shop_id = forms.IntegerField(label='ショップコード',widget=forms.NumberInput(attrs={
        'placeholder':1,
        'class':'form-control'
        }))

    positions = [
        (False,'キッチン'),
        (True,' ホール')
    ]

    default_position = forms.ChoiceField(label='ポジション',choices=positions,widget=forms.Select(attrs={
        'class':'form-control'
    }))
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password1',
            'password2',
            'shop_id',
            'default_position',
        ]
        widgets = { 
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password1':forms.TextInput(attrs={'class':'form-control'}),
            'password2':forms.TextInput(attrs={'class':'form-control'}),
            'shop_id':forms.NumberInput(attrs={'class':'form-control'}),
            'default_position':forms.Select(attrs={'class':'form-control'}),
            }
