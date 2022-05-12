from django.urls import path
from . import views

app_name = 'ShiftManagementApp'
urlpatterns = [
    path('',views.home,name = 'index'),
    path('home/',views.home,name = 'index'),
    path('login/',views.Login,name = 'Login'),
    path('logout/',views.Logout,name ='Logout'),
    path('create-newaccount/',views.create_newaccount,name='create-newaccount'),
    #path('SubmitShift/',views.SubmitShift.as_view(),name = 'SubmitShift'),
    path('SubmitShift-Ajax/',views.submitshift,name='SubmitShift-Ajax'),
    path('edit-shift/',views.editshift,name='edit-shift'),
    path('edit-shift-Ajax/',views.editshift_ajax,name='edit-shift-Ajax'),
    path('edit-shift-Ajax/post-shiftdata/',views.editshift_ajax_post_shiftdata,name='edit-shift-Ajax-post-shiftdata'),
    path('edit-shift-Ajax/delete-shiftdata/',views.editshift_ajax_delete_shiftdata,name='edit-shift-Ajax-delete-shiftdata'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'), 
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'), 
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'), 
    path('contact/',views.contact,name="contact"),
    path('contact/done/',views.contact_success,name="contact_success")
]