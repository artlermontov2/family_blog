from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.loginuser, name='loginuser'),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('blogs/', views.blogentry, name='blogentry'),
    path('create/', views.createblog, name='createblog'),
    # path('<int:blog_id>/', views.blogdetail, name='blogdetail'),
    path('<int:pk>/', views.BlogView.as_view(), name='blogdetail'),
    path('<int:blog_id>/delete', views.deleteblog, name='deleteblog'),
    path('<int:pk>/edit', views.EditBlog.as_view(), name='editblog'),
]