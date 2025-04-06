from django.urls import path
from django.urls import include
from .views import *


urlpatterns = [
    path('', my_profile, name="profile"),
    path('logout/', logout_view, name="logout"),
    path('add_post/', add_post, name="add_post"),
    path('post/<str:post_id>/', post_detail, name="post_detail"),
    path('author/<str:author_id>/', author_profile, name="author"),
    path('place/', list_place, name="list_place"),
    # path('place/<str:place_id>/', place_detail, name="place_detail"),
    path('create/', create_playlist, name='create_playlist'),
    path('post-list/<str:place_id>/', post_list, name="post_list"),
]
