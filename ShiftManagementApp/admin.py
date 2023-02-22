from django.contrib import admin
from ShiftManagementApp.models import User, Shift,Shift_Archive,Contact,LINE_USER_ID,Deadline

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','shop_id','username','email','is_edit_mode','is_staff','is_active']

class ShiftAdmin(admin.ModelAdmin):
    list_display = ['user','date','begin','finish','position','publish']

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