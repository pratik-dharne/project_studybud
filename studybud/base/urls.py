from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('',views.home,name='home'),
    path('room/<int:pk>/',views.room,name='room'),
    path('create-room/',views.createroom,name='create-room'),
    path('update-room/<int:pk>/',views.updateroom,name='update-room'),
    path('delete-room/<int:pk>/',views.deleteroom,name='delete-room'),
    path('delete-message/<int:pk>/',views.deletemessage,name='delete-message'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('profile/<int:pk>',views.userprofile,name='user-profile'),
    path('register/',views.register_page,name='register'),
    path('update-user/',views.updateuser,name='update-user'),
    path('topics/',views.topicspage,name='topics-page'),
    path('activity/',views.activitypage,name='activity-page'),

    path('password-reset/',
        auth_views.PasswordResetView.as_view(template_name='base/password_reset.html'),
        name='password_reset'),

    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_done.html'),
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='base/password_reset_confirm.html'),
        name='password_reset_confirm'),

    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_complete.html'),
        name='password_reset_complete')

]