import django_filters
from rest_framework import filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'title':['icontains'],
            'author__username':['icontains'],
            'created_at':['date__gte','date__lte'],
        }