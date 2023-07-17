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
            'title':'Register'
        }
        return render(request, 'user/user_register.html',context)
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('user:login')
        form.add_error(None, '잘못된 입력입니다.')

        context ={
                'form':form
            }

        return render(request, 'user/user_register.html', context)


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
        if request.user.is_authenticated:
            return redirect('diary:list')
        
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('diary:list')
            
        form.add_error(None, '해당 계정은 존재하지 않습니다.')

        context ={
                'form':form
            }

        return render(request, 'user/user_login.html', context)


# 로그아웃
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('diary:list')