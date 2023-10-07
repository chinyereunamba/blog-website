from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),


    # path('create-post/', CreatePost.as_view(), name='create-post'),
    path('create-post/', createPost, name='create_post'),
    path('update-post/<slug:slug>', updatePost, name='update_post'),
    path('delete-post/<slug:slug>', deletePost, name='delete_post'),

    path('posts/', posts, name='posts'),
    path('posts/<slug:slug>/', viewPost, name='post'),

    path('category/', category, name="category"),
    path('category/<slug:slug>/', categoryList, name="categoryList"),

    path('tag/<slug:slug>/', tags, name="tags"),

    path('create-tag/', CreateTag.as_view(), name='create_tag'),
    path('create-category/', CreateCategory.as_view(), name='create_category'),

    path('contact/', contact, name="contact"),

    path('about/', about, name="about"),
    path('newsletters/', thanks, name="thanks"),

    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),

]
