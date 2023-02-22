from django.contrib import admin
from django_admin_relation_links import AdminChangeLinksMixin
from ShiftManagementApp.models import User, Shift,Shift_Archive,Contact,LINE_USER_ID,Deadline

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','shop_id','username','email','is_edit_mode','is_staff','is_active']

class ShiftAdmin(AdminChangeLinksMixin,admin.ModelAdmin):
    list_display = ['user','user_name','user_shop_id','date','begin','finish','position','publish']
    change_links = ['user']

    def user_name(self,obj):
        return obj.user.username
    user_name.short_description = 'ユーザー名'

    def user_shop_id(self,obj):
        return obj.user.shop_id
    user_shop_id.short_description = 'shop_id'
    user_shop_id.admin_order_field = 'user__shop_id'

class LineAdmin(admin.ModelAdmin):
    list_display = ['user','line_user_id']

class DeadLineAdmin(admin.ModelAdmin):
    list_display = ['shop_id','deadline']
admin.site.register(User,UserAdmin)
admin.site.register(Shift_Archive,ShiftAdmin)
admin.site.register(Shift,ShiftAdmin)
admin.site.register(Contact)
admin.site.register(LINE_USER_ID,LineAdmin)
admin.site.register(Deadline,DeadLineAdmin)