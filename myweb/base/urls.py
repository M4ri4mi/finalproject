from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/update/', views.task_update, name='task_update'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('register/', views.register_page, name='register')
]




