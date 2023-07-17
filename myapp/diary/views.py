from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment
from .forms import PostForm, CommentForm

from django.template.defaulttags import register
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
    

class Write(View):
    def get(self, request):
        form = PostForm()
        context = {
            'form':form,
            'title':"오늘의 일기"
        }
        return render(request, 'diary/post_write.html', context)
    
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer = request.user
            post.save()
            return redirect('diary:detail', pk=post.pk)
        form.add_error(None, '입력이 유효하지 않습니다!')
        context ={
            'form':form
        }
        return render(request, 'diary/post_write.html', context)
    

@register.filter
def get_mood_icon(moodscore):
    MOOD_CHOICES = {
    5 : '❤️❤️❤️❤️❤️',
    4 :'💛💛💛💛',
    3 :'💚💚💚' ,
    2 :'💙💙',
    1 :'💜'
    }
    return MOOD_CHOICES[moodscore]


class Detail(View):
    def get(self, request,pk):
        post = Post.objects.prefetch_related('comment_set').get(pk=pk)
        comments = post.comment_set.all()
        comment_form = CommentForm()

        context ={
            'title':'일기',
            'post_id':pk,
            'post_title':post.title,
            'post_date':post.date,
            'post_writer':post.writer,
            'post_mood': get_mood_icon(post.mood),
            'post_content':post.content,
            'comments':comments,
            'comment_form':comment_form,
        }
        return render(request, 'diary/post_detail.html', context)
    

class Delete(View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('diary:list')

class Update(View):
    def get(self, request,pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(
            initial= {
                'title': post.title,
                'content':post.content,
                'mood':post.mood
            })
        context = {
            'form':form,
            'post':post,
            'title':(str)(post.date) +'의 일기'
        }
        return render(request, 'diary/post_edit.html', context)
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST)
        if form.is_valid():
            post.title=form.cleaned_data['title']
            post.content=form.cleaned_data['content']
            post.mood=form.cleaned_data['mood']
            
            post.save()
            return redirect('diary:detail', pk=pk)
        form.add_error('입력이 유효하지 않습니다.')
        context ={
            'form':form,
            'title': '일기'
        }
        return render(request, 'diary/post_edit.html',context)


### Comment

class CommentWrite(View):
    def post(self, request, pk):
        pass


class CommentEdit(View):
    def get(self, request, commentID):
        pass
    def post(self, request, commentID):
        pass

    
class CommentDelete(View):
    def post(self, request, commentID):
        pass
