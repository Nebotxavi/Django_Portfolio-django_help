from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('results/', views.SearchResultsView.as_view(), name='results'),
    path('posts/<str:username>/',
         views.UserPostListView.as_view(), name='user_posts'),
    path('posts/tags/<str:tag>/', views.TagPostListView.as_view(), name='tag_posts'),
    path('post/new_post/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/',
         views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/',
         views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<slug:slug>/', views.PostDetailView, name='post_detail'),

]
