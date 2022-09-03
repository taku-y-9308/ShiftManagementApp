from django.contrib import admin
from ShiftManagementApp.models import User, Shift,Shift_Archive,Contact,LINE_USER_ID

admin.site.register(User)
admin.site.register(Shift_Archive)
admin.site.register(Shift)
admin.site.register(Contact)
admin.site.register(LINE_USER_ID)