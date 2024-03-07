# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('list_movie', views.list_movie, name='movie_list'),
    path('add_show/', views.add_show, name='add_show'),
    path('edit_show/<int:show_id>/', views.edit_show, name='edit_show'),
    path('delete_show/<int:show_id>/', views.delete_show, name='delete_show'),
    path('disable_show/<int:show_id>/', views.disable_show, name='disable_show'),
    path('show_list', views.show_list, name='list_show'),
    path('signup/', views.signup, name='signup'),
    path('', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # Add similar patterns for other views (add_show, edit_show, delete_show, disable_show)
]


