from django.urls import path

from . import views

urlpatterns = [
    # login url
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),


    path('room-create', views.createRoom, name='room-create'),
    path('room-update/<str:pk>/', views.updateRoom, name='room-update'),
    path('room-delete/<str:pk>/', views.deleteRoom, name='room-delete'),
    path('message-delete/<str:pk>/', views.deleteMessage, name='message-delete'),
]
