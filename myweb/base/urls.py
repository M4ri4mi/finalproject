from django.urls import path
from . import views
from .views import create_plan, update_plan, delete_plan, plan_list


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/update/', views.task_update, name='task_update'),
    path('task/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('plan/create/', views.create_plan, name='create-plan'),
    path('plan/update/<int:pk>/', views.update_plan, name='update-plan'),
    path('plan/delete/<int:pk>/', views.delete_plan, name='delete-plan'),
    path('register/', views.register_page, name='register'),
    path('accounts/login/', views.login_view, name='accounts_login')
]






