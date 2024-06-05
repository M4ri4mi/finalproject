from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name= 'logout'),
    path('profile/', views.profile, name='profile'),
    path('add_task/', views.add_task, name='add_task')

]
