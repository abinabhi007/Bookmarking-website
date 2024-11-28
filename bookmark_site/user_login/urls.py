from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home,name='home'),
    path('edit-bookmark/<int:bookmark_id>/', views.edit_bookmark, name='edit_bookmark'), 
    path('delete-bookmark/<int:id>/', views.delete_bookmark, name='delete_bookmark'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('my_collections/', views.my_collections, name='my_collections'),
    path('bookmark_list/', views.bookmark_list,name='bookmark_list'),
]
