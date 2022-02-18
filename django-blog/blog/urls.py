from django.urls import path, re_path

from . import views

app_name = 'blog'
urlpatterns = [
    path( '', views.IndexView.as_view(), name='index'),
    path( 'search_by_<search>/', views.SearchIndexView.as_view(), name='search'),
    path( 'register/', views.Register, name='register'),
    path( 'update_profile/', views.UpdateProfile.as_view(), name='update_profile'),
    path( 'create_category/<option>/', views.CreateCategory.as_view(), name='new_category'),
    path( 'create_post/', views.CreatePost.as_view(), name='new_post'),
    path( '<int:post_id>/', views.DetailListView.as_view(), name='post_details'), 
    path( '<int:post_id>/update_post/', views.UpdatePost.as_view(), name='update_post'),
    path( '<int:post_id>/delete_post/', views.DeletePost.as_view(), name='delete_post'), 
    path( '<int:post_id>/', views.DetailListView.as_view(), name='comments_list'),  
    path( '<int:post_id>/create_comment/', views.CreateComment.as_view(), name='new_comment'), 
    path( '<int:post_id>/<int:comment_id>/update_comment/', views.UpdateComment.as_view(), name='update_comment'),
    path( '<int:post_id>/<int:comment_id>/delete_comment/', views.DeleteComment.as_view(), name='delete_comment'), 
 
]