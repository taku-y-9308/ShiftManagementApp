from email.policy import default
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Emailを入力して下さい')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_staff=Trueである必要があります。')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser=Trueである必要があります。')
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    shop_id = models.IntegerField("shop_id")
    username = models.CharField("username", max_length=50, validators=[username_validator])
    default_position = models.BooleanField("default_position")
    email = models.EmailField("email_address", unique=True)
    is_staff = models.BooleanField("staff status", default=False) #スタッフユーザー（管理者）かどうか
    is_active = models.BooleanField("active", default=True) #退職したユーザーはFalse
    date_joined = models.DateTimeField("date joined", default=timezone.now) #アカウント作成日

    objects = UserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['shop_id','username','default_position']

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
    '''
    def __int__(self):
        return self.pk
    '''


class Shift(models.Model):
    #foreignkeyに指定したUserはUserクラスがリターンしたやつを受け取っている
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="ユーザーID",related_name='shift')
    date = models.DateField("date")
    begin = models.DateTimeField("begin")
    finish = models.DateTimeField("finish")
    position = models.BooleanField("position")
    def __str__(self):
        return str(self.date)

    '''
    class User(models.Model):
    user_id = models.IntegerField(verbose_name="ユーザーID")
    name = models.CharField(max_length=100, verbose_name="名前")
    def __int__(self): 
        return self.user_id
    '''

class Contact(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="ユーザーID")
    title = models.CharField("title",max_length=50)
    text = models.CharField("text",max_length=1000)
    def __str__(self):
        return str(self.title)