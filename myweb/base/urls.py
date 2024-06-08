from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('note/<int:note_id>/update/', views.update_note, name='update-note'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete-note'),
    path('register/', views.register_page, name='register'),
    path('accounts/login/', views.login_view, name='accounts_login')
]








