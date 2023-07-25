from django.shortcuts import render, redirect
from django.views import View
from .models import Post, Comment
from .forms import PostForm, CommentForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.template.defaulttags import register

import base64
import io
# from PIL import Image
# from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from rest_framework import serializers


# 로그 남기기
import logging
logger = logging.getLogger('django')
# Create your views here.

# Post
# 전체 게시물 보여줌


class ListView(View):
    def get(self, request):
        post_objs = Post.objects.all()
        context = {
            "posts": post_objs,
            "title": "전체 게시물"
        }
        return render(request, 'diary/post_list.html', context)


# def decodeDesignImage(imageURL):  # B64 -> PIL 이미지 변환
#     try:
#         data = base64.b64decode(data.encode('UTF-8'))
#         buf = io.BytesIO(data)
#         img = Image.open(buf)
#         return img
#     except:
#         logger.info("이미지 변환 실패")
#         return None

class Base64ImageField(serializers.ImageField):
    def from_native(self, data):
        if isinstance(data, basestring) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super(Base64ImageField, self).from_native(data)


class Write(View):
    def get(self, request):
        # form = PostForm()
        context = {
            # 'form': form,
            'title': "오늘의 일기"
        }
        return render(request, 'diary/post_write.html', context)

    def post(self, request):
        logger.info("views.py입니다")
        title = request.POST.get('title')
        content = request.POST.get('content')
        imgURL = request.POST.get('imgURL')
        logger.info(imgURL)
        img = Base64ImageField(imgURL)
        img.save(img, format='png')
        mood = request.POST.get('mood')
        post = Post(title=title, content=content,
                    writer=request.user, painting=img, mood=mood)
        post.save()
        context = {
            'post_date': post.date,
            'post_title': post.title,
            'post_writer': post.writer,
            'post_mood': post.mood,
            'post_content': post.content,
            'post_painting': post.painting
        }

        return render(request, 'diary/post_write.html', context)

        # form = PostForm(request.POST.data)
        # form = request.POST.data
        # logger.info(request.POST)
        # if form.is_valid():
        #     post = form.save(commit=False)
        #     post.writer = request.user
        #     data = request.POST.data.__getitem__('data')
        #     logger.info(data)
        #     data = data[22:]  # 앞의 헤더 제거

        #     img = base64.b64decode(data)
        #     post.painting = img
        #     post.save()
        #     return redirect('diary:detail', pk=post.pk)
        # form.add_error(None, '입력이 유효하지 않습니다!')
        # context = {
        #     'form': form
        # }
        # return render(request, 'diary/post_write.html', context)


@register.filter
def get_mood_icon(moodscore):
    MOOD_CHOICES = {
        5: '❤️❤️❤️❤️❤️',
        4: '💛💛💛💛',
        3: '💚💚💚',
        2: '💙💙',
        1: '💜'
    }
    return MOOD_CHOICES[moodscore]


class Detail(View):
    def get(self, request, pk):
        post = Post.objects.prefetch_related('comment_set').get(pk=pk)
        comments = post.comment_set.all()
        comment_form = CommentForm()

        context = {
            'title': '일기',
            'post_id': pk,
            'post_title': post.title,
            'post_date': post.date,
            'post_writer': post.writer,
            'post_mood': get_mood_icon(post.mood),
            'post_painting': post.painting,
            'post_content': post.content,
            'comments': comments,
            'comment_form': comment_form,
        }
        return render(request, 'diary/post_detail.html', context)


class Delete(View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('diary:list')


class Update(View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(
            initial={
                'title': post.title,
                'content': post.content,
                'mood': post.mood
            })
        context = {
            'form': form,
            'post': post,
            'title': (str)(post.date) + '의 일기'
        }
        return render(request, 'diary/post_edit.html', context)

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.mood = form.cleaned_data['mood']

            post.save()
            return redirect('diary:detail', pk=pk)
        form.add_error('입력이 유효하지 않습니다.')
        context = {
            'form': form,
            'title': '일기'
        }
        return render(request, 'diary/post_edit.html', context)


# Comment

class CommentWrite(View):
    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Post.objects.get(pk=pk)
        if form.is_valid():
            content = form.cleaned_data['content']
            writer = request.user

            try:
                comment = Comment.objects.create(
                    post=post, content=content, writer=writer)
                # 생성할 값이 이미 있다면 오류 발생, unique 값이 중복될 때
                # 필드 값이 비어있을 때 : ValidationError
                # 외래 키 관련 데이터베이스 오류 : ObjectDoesNotExist

            except ObjectDoesNotExist as e:
                print('존재하지 않는 글입니다.', str(e))

            except ValidationError as e:
                print('로그인되어있지 않습니다.')

            return redirect('diary:detail', pk=pk)

        context = {
            'title': '일기',
            'post': post,
            'comments': post.comment_set.all(),
            'comment_form': form,
        }
        return render(request, 'diary/post_detail.html', context)


class CommentEdit(View):
    def get(self, request, commentID):
        pass

    def post(self, request, commentID):
        pass


class CommentDelete(View):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        post_id = comment.post.id
        comment.delete()
        return redirect('diary:detail', pk=post_id)
