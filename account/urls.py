from django.urls import path
from. import views


urlpatterns = [
    path('register/', views.registerview, name='register'),
    path('login/', views.loginview, name='login'),
    path('home/', views.homeview, name='users-home'),
    path('logout/', views.logoutview, name='logout'),
    path('profile/', views.userprofileview, name='users-profile'),

]