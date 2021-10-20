from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    path('', views.home,name='home'),
    path('about/', views.about,name='about'),
    path('login/', views.loginpage,name='login'),
    path('register/', views.registerPage,name='register'),
    path('logout/', views.userLogout,name='logout'),
    path('room/<str:pk>',views.room,name='room'),
    path('create-room/',views.createRoom,name='createRoom'),
    # path('create-msg/',views.createMessage,name='createMessage'),
    path('create-topic/',views.createTopic,name='createTopic'),
    path('update-room/<str:pk>',views.updateRoom,name='updateRoom'),
    path('delete-room/<str:pk>',views.deleteRoom,name='deleteRoom'),
    path('delete-message/<str:pk>',views.deleteMessage,name='deleteMessage'),
]