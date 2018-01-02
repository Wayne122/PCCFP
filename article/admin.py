from django.contrib import admin
from .models import Article, Comment, Follow

# Register your models here.

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Follow)