from django.contrib import admin
from .models import Category, Author, Post, Comment, Reply
from hitcount.models import HitCount, BlacklistIP, BlacklistUserAgent, Hit
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
# admin.site.register(Reply)
# admin.site.unregister(Hit)
# admin.site.unregister(HitCount)
# admin.site.unregister(BlacklistIP)
# admin.site.unregister(BlacklistUserAgent)