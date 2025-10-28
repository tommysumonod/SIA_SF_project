from django.urls import path
from . import views

urlpatterns = [
    # ---------------- HERO / LANDING ---------------- #
    path('', views.hero, name='hero'),

    # ---------------- PROFILE ---------------- #
    path('profile/', views.profile, name='profile'),
    path('profile/<str:uid>/', views.view_profile, name='view_profile'),

    # Profile updates
    path("upload-profile-picture/", views.upload_profile_picture, name="upload_profile_picture"),
    path("update-profile-bio/", views.update_profile_bio, name="update_profile_bio"),
    path('update_profile_pic/', views.update_profile_pic, name='update_profile_pic'),

    # ---------------- GALLERY / UPLOADS ---------------- #
    path('gallery/', views.gallery, name='gallery'),
    path('create/', views.create, name='create'),
    path('upload-art/', views.upload_art, name='upload_art'),
    path('art/<str:art_id>/', views.upload_view, name='upload_view'),   # ✅ single source of truth
    path('art/<str:art_id>/edit/', views.edit_art, name='edit_art'),
    path('art/<str:art_id>/comment/', views.post_comment, name='post_comment'),
    path('uploads/', views.all_uploads, name='all_uploads'),
    path('search/', views.search_artworks, name='search_artworks'),
    path('category/<str:category_name>/', views.category_view, name='category_view'),
    path('art/<str:art_id>/delete/', views.delete_art, name='delete_art'),


    # ---------------- AUTH ---------------- #
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_page, name='signin'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ---------------- CHAT SYSTEM ---------------- #
    path('chat/', views.chat_home, name='chat_home'),
    path('chat/<str:uid>/', views.chat_with_user, name='chat_with_user'),
    path('chat/<str:uid>/send/', views.send_message, name='send_message'),
    path('chat/<str:uid>/fetch/', views.fetch_messages, name='fetch_messages'),
]
