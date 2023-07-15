from django.urls import path
from . import views

app_name = 'diary'
urlpatterns = [
    # 모두의 일기 조회
    path("", views.ListView.as_view(), name="list"),
]