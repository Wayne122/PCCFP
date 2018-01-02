from django.shortcuts import render
from .models import Article, Comment, Follow, Read_History
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

# Create your views here.
def home(request):
    article_list = Article.objects.all()
    return render(request, 'home.html', {
        'article_list': article_list,
    })

def account(request):
    user_list = UserSocialAuth.objects.all()
    return render(request, 'account.html', {'sau': user_list})

def article(request, pk):
    if request.user.is_authenticated:
        if Read_History.objects.filter(article=Article.objects.get(pk=pk), reader=request.user).count() == 0:
            Read_History.objects.create(article=Article.objects.get(pk=pk), reader=request.user)
    article = Article.objects.get(pk=pk)
    comments = Comment.objects.filter(article=article)
    recommendation = None
    if request.user.is_authenticated:
        users_read = Read_History.objects.filter(article=article).exclude(reader=request.user)
        article_id = []
        for user_read in users_read:
            articles_read = Read_History.objects.filter(reader=user_read.reader).exclude(article=article)
            for article_read in articles_read:
                if article_read.article.id not in article_id and article_read.article.author != request.user:
                    article_id.append(article_read.article.id)
        recommendation = Article.objects.filter(id__in=article_id)

    return render(request, 'article.html', {'article': article, 'comments': comments, 'recommendation': recommendation})

def author_works(request, pk):
    author = User.objects.get(pk=pk)
    if request.user.is_authenticated:
        follower = Follow.objects.filter(author=User.objects.get(pk=pk), reader=request.user)
    else:
        follower = None
    return render(request, 'author_works.html', {'author': author, 'works': author.article_set.all(), 'follower': follower})

from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'photo']
        exclude = ('author',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ArticleForm(request.POST)
            if form.is_valid():
                new_article = form.save(commit=False)
                new_article.author = request.user
                new_article = form.save()
                return HttpResponseRedirect('/article/' + str(new_article.pk))

        form = ArticleForm()
        return render(request, 'create_article.html', {'form': form})
    else:
        return auth_views.login(request)

def edit(request, pk):
    if request.user.is_authenticated and Article.objects.get(pk=pk).author == request.user:
        article = Article.objects.get(pk=pk)
        form = ArticleForm(request.POST or None, instance=article)
        if request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect('/article/' + str(pk))

        return render(request, 'create_article.html', {'form': form})
    else:
        return HttpResponseForbidden()

def follow(request, pk):
    if request.user.is_authenticated:
        if Follow.objects.filter(author=User.objects.get(pk=pk), reader=request.user).count() == 0 and pk != str(request.user.id):
            Follow.objects.create(author=User.objects.get(pk=pk), reader=request.user)
        return HttpResponseRedirect('/author/' + pk)
    else:
        return auth_views.login(request)

def unfollow(request, pk):
    if request.user.is_authenticated:
        if Follow.objects.filter(author=User.objects.get(pk=pk), reader=request.user).count() == 1:
            Follow.objects.get(author=User.objects.get(pk=pk), reader=request.user).delete()
        return HttpResponseRedirect('/author/' + pk)
    else:
        return auth_views.login(request)

def follow_list(request):
    if request.user.is_authenticated:
        follow_list = Follow.objects.filter(reader=request.user)
        return render(request, 'follow_list.html', {'follow_list': follow_list})
    else:
        return auth_views.login(request)

def comment(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.user = request.user
                new_comment.article = Article.objects.get(pk=pk)
                form.save()
                return HttpResponseRedirect('/article/' + str(pk))

        form = CommentForm()
        return render(request, 'create_comment.html', {'form': form})
    else:
        return auth_views.login(request)