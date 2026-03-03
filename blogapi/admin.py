from django.contrib import admin

from blogapi.models import Post, User

# Register your models here.
admin.site.register(User)
admin.site.register(Post)