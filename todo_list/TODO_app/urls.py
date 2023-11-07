from django.contrib import admin
from django.urls import path
from .views import taskList,detailList,createList,updateList,deleteList,userLogin,registerView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/',userLogin.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page = 'login'), name='logout'),
    path('register/',registerView.as_view(), name='register'),
    path('',taskList.as_view(), name='task-list'),
    path('task/<int:pk>/',detailList.as_view(), name='view'),
    path('create/',createList.as_view(), name='create'),
    path('update/<int:pk>/',updateList.as_view(), name='update'),
    path('delete/<int:pk>/',deleteList.as_view(), name='delete'),
]