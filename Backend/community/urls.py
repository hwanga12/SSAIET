from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.post_list_create),
    # ✅ 카테고리별 목록 조회를 위한 URL 추가
    path("category/<str:category>/", views.community_list_by_category),
    path("my-comments/", views.my_comments_list),
    path("posts/<int:post_id>/", views.post_detail),
    path("posts/<int:post_id>/like/", views.toggle_like),
    path('posts/<int:post_id>/comments/', views.comment_list_create),
    path('comments/<int:pk>/', views.comment_update_delete),
]