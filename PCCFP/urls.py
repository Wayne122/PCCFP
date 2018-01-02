"""PCCFP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from article.views import home, account, article, create, author_works, follow, unfollow, follow_list, comment, edit

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^account_detail/', account, name='account_detail'),
    url(r'^article/(?P<pk>\d+)/$', article, name='article_detail'),
    url(r'^create/$', create, name='create_article'),
    url(r'^author/(?P<pk>\d+)/$', author_works, name='author'),
    url(r'^follow/(?P<pk>\d+)/$', follow, name='follow'),
    url(r'^unfollow/(?P<pk>\d+)/$', unfollow, name='unfollow'),
    url(r'^follow_list/$', follow_list, name='follow_list'),
    url(r'^article/(?P<pk>\d+)/comment/$', comment, name='comment'),
    url(r'^article/(?P<pk>\d+)/edit/$', edit, name='edit_article'),
]
