from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    # 모든 일기 조회
    path("", views.ListView.as_view(), name="list"),
    # 글 작성
    path("write/", views.Write.as_view(), name='write'),
    # 글 상세 페이지
    path("detail/<int:pk>/", views.Detail.as_view(), name='detail'),
    # 글 삭제
    path("detail/<int:pk>/delete/", views.Delete.as_view(), name='delete'),
    # 글 수정
    path("detail/<int:pk>/edit/", views.Update.as_view(), name='edit'),

    # 댓글
    # 댓글 작성
    path("detail/<int:pk>/comment/write/",
         views.CommentWrite.as_view(), name="cm-write"),
    # 댓글 삭제
    path("detail/<int:pk>/comment/delete/",
         views.CommentDelete.as_view(), name="cm-delete"),
    # 댓글 수정
    # path("detail/<int:pk>/comment/edit/",
    #      views.CommentEdit.as_view(), name="cm-edit")
]
