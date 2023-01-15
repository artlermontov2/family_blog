from django.shortcuts import render
from django.db import IntegrityError
from django.views.generic import UpdateView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # шаблон формы регистрации, аутентификации
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from .models import Blog
from .forms import BlogForm
from django.contrib.auth.decorators import login_required  # Декоратор будет выводить сообщение о том, что только зарег. пользователи могут видеть эту страницу


def home(request):
    return render(request, 'blog/home.html', {})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'blog/signupuser.html', {'form': UserCreationForm()})
    else:
        # Создание нового пользователя
        # Проверка пароля 1 и пароля 2, только после этого переходить к регистрации
        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password'])  # Создаст объект
                user.save()  # Сохраняет объект
                login(request, user)
                return redirect(
                    'blogentry')  # после того, как пользователь ввёл логин мы должны отправить его на страницу c записями
            except IntegrityError:
                # Если имя нового пользователя уже есть в базе
                return render(request, 'blog/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'Ой, это имя уже используется :-('})
        else:
            return render(request, 'blog/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})
            # Сообщение о том, что пароли не совпадают


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'blog/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'blog/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Пользователь с таким именем не зарегистрирован'})
        else:
            login(request, user)
            return redirect('blogentry')


@login_required
def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('loginuser')


@login_required
def blogentry(request):
    blogs = Blog.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'blog/blogentry.html', {'blogs': blogs})


# @login_required
# def blogdetail(request, blog_id):
#     blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
#     return render(request, 'blog/blogdetail.html', {'blog': blog})
class BlogView(DetailView):
    model = Blog
    template_name = 'blog/blogdetail.html'


@login_required
def createblog(request):
    if request.method == 'GET':
        return render(request, 'blog/createblog.html', {'form': BlogForm()})
    else:
        try:
            form = BlogForm(request.POST)
            newblog = form.save(commit=False)
            newblog.user = request.user
            newblog.save()
            return redirect('blogentry')
        except ValueError:
            return render(request, 'blog/createblog.html',
                          {'form': BlogForm(), 'error': 'Превышено допустимое кол-во символов'})


def deleteblog(request, blog_id):  # удаление записи
    blog = get_object_or_404(Blog, pk=blog_id, user=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('blogentry')


class EditBlog(UpdateView):
    model = Blog
    fields = ['title', 'description']
    template_name = 'blog/editblog.html'
