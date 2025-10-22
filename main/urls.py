from django.urls import path
from . import views

urlpatterns = [
    path('', views.hero, name='hero'),
    path('profile/', views.profile, name='profile'),
    path('gallery/', views.gallery, name='gallery'),
    path('chat/', views.chat, name='chat'),
    path('uploads/', views.uploads, name='uploads'),
    # signup page handled by signup_view (GET renders form, POST creates user)
    path('signin/', views.signin_page, name='signin'),
    path('create/', views.create, name='create'),
    path("upload-profile-picture/", views.upload_profile_picture, name="upload_profile_picture"),
    path("update-profile-bio/", views.update_profile_bio, name="update_profile_bio"),
    path("upload-view/", views.update_profile_bio, name="upload_view"),

    # Auth routes
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
