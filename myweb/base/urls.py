from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('note/<int:note_id>/update/', views.update_note, name='update_note'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('task/<int:task_id>/update/', views.update_task, name='update_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/toggle_done/', views.toggle_task_done, name='toggle_task_done'),
    path('project/<int:project_id>/update/', views.update_project, name='update_project'),
    path('project/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('project/<int:project_id>/toggle_done/', views.toggle_project_done, name='toggle_project_done'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_results, name='search_results'),

]








