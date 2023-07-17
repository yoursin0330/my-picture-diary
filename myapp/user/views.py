from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm, LoginForm
# Create your views here.

# 회원가입
class Registeration(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('diary:list')
        # 로그인 x -> 회원가입 페이지
        form = RegisterForm()
        context ={
            'form':form,
            'title':'User'
        }
        return render(request, 'user/user_register.html',context)
    def post(self, request):
        pass


# 로그인
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('diary:list')
        form = LoginForm()
        context ={
            'form':form,
            'title':'Login'
        }
        return render(request, 'user/user_login.html', context)
    def post(self, request):
        pass


# 로그아웃
class Logout(View):
    def post(self, request):
        logout(request)
        return redirect('diary:list')