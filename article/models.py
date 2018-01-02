from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    photo = models.URLField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    edited_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        UserName = ''
        for auser in User.objects.all():
            if auser.id == self.user_id:
                UserName = auser.username
        return UserName

class Follow(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_followed')
    reader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reader_follows')

class Read_History(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reader = models.ForeignKey(User, on_delete=models.CASCADE)