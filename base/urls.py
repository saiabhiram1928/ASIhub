from django.urls import path
from . import views

urlpatterns = [
    path('',views.home , name= 'home'),
    path('room/<str:pk>',views.room , name= 'room'),
    path('createRoom/',views.createRoom , name= 'room_form'),
    path('joinRoom/<str:pk>',views.joinRoom , name= 'join_room'),
    path('updateRoom/<str:pk>',views.updateRoom , name= 'update_room_form'),
    path('delete/<str:pk>',views.deleteRoom , name= 'delete_room'),
    path('delete_msg/<str:pk>',views.delete_msg , name= 'delete_msg'),
    path('login/',views.loginUser , name= 'login'),
    path('register/',views.register , name= 'register'),
    path('profile/<str:pk>',views.profile , name= 'profile'),
    path('logout/',views.logoutUser , name= 'logout'),
    path('updateUser/',views.updateUser , name= 'update_user'),
    path('updateProfile/',views.updateProfile , name= 'update_profile'),
    path('go_back/',views.go_back , name= 'go_back'),
    path('topics/',views.topicsPage , name= 'topics'),
    path('activity/',views.activityPage , name= 'activity'),
]
