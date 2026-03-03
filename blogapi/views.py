from django.shortcuts import render
from rest_framework import  viewsets,generics,filters,permissions
from .models import User, Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

class UserViewSet(viewsets.ModelViewSet):
    queryset =User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email']
    
    #problem in geting normal user data
    def get_queryset(self):
         qs = super().get_queryset()
         if not self.request.user.is_staff:
               qs = qs.filter(id=self.request.user.id)
         return qs

class PostViewSet(viewsets.ModelViewSet):
     queryset = Post.objects.all()
     serializer_class = PostSerializer
     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
     filter_backends = [filters.SearchFilter,filters.OrderingFilter]
     search_fields = ['title', 'content']
     ordering_fields = ['created_at', 'updated_at']
     def perform_create(self, serializer):
          serializer.save(author=self.request.user)
     def destroy(self, request, *args, **kwargs):
          
     #@action(detail=True,methods=['post'],permission_classes=[permissions.IsAuthenticated])





