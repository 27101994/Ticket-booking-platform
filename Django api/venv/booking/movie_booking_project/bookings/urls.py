# bookings/urls.py
from django.urls import path
# from .views import add_movie, edit_movie, delete_movie, add_show, edit_show, delete_show, disable_show
# from .views import signup, login, show_list, book_show, my_bookings, download_ticket
from . import views
# bookings/urls.py


urlpatterns = [
    # path('signup_admin/', views.signup_admin),
    # path('login_admin/', views.login_admin),
    # path('add_movie/', views.add_movie),
    # path('edit_movie/<int:movie_id>/', views.edit_movie),
    # path('delete_movie/<int:movie_id>/', views.delete_movie),
    # path('add_show/', views.add_show),
    # path('edit_show/<int:show_id>/', views.edit_show),
    # path('delete_show/<int:show_id>/', views.delete_show),
    # path('disable_show/<int:show_id>/', views.disable_show),
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout, name='logout'),
    path('movie_list/', views.list_movie, name='movie_list'),
    path('show_list/<int:movie_id>/', views.show_list),
    path('book_show/<int:show_id>/', views.book_show),
    path('conf_show/<int:booking_id>/', views.confirmation),
    path('my_bookings/', views.my_bookings),
    # path('send_mail/<int:movie_id>/', views.send_product_email_api),
    path('generate_pdf/<int:id>/', views.generate_pdf),
    # path('download_ticket/<int:booking_id>/', views.download_ticket),
]


