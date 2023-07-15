from django.shortcuts import render
from django.views import View
# Create your views here.

### Post
# 전체 게시물 보여줌
class ListView(View):
    def get(self, request):
        post_objs = Post.objects.all()
        context ={
            "posts" : post_objs,
            "title" : "전체 게시물"
        }
        return render(request, 'diary/post_list.html', context)