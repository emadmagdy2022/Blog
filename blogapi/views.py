from django.shortcuts import render
from rest_framework import  generics,filters,permissions
from .models import User, Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer

class UserViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email']