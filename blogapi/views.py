from django.shortcuts import render
from rest_framework import  viewsets,generics,filters,permissions
from .models import User, Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

class UserViewSet(viewsets.ModelViewSet):
    queryset =User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email']
    
    
    def get_queryset(self):
         qs = super().get_queryset()
         if not self.request.user.is_staff:
               qs = qs.filter(id=self.request.user.id)
         return qs


class PostViewSet(viewsets.ModelViewSet):
     queryset = Post.objects.prefetch_related('comments','likes','author')
     serializer_class = PostSerializer
     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
     filter_backends = [filters.SearchFilter,filters.OrderingFilter]
     search_fields = ['title', 'content']
     ordering_fields = ['created_at', 'updated_at']

     @method_decorator(cache_page(60*15, key_prefix='post_list'))
     def list(self, request, *args, **kwargs):
          return super().list(request, *args, **kwargs)
     
     def perform_create(self, serializer):
          serializer.save(author=self.request.user)

     def destroy(self, request, *args, **kwargs):

          requestUser = request.user
          postAuthor = self.get_object().author
          if requestUser.is_staff or postAuthor == requestUser:
               with transaction.atomic():
                    instance = self.get_object()
                    instance.comments.all().delete()
                    instance.likes.all().delete()
               return super().destroy(request, *args, **kwargs)
          else:
               return Response({'detail': 'You do not have permission to delete this post.'}, status=403)
     
     def update(self, request, *args, **kwargs):
          requestUser = request.user
          postAuthor = self.get_object().author
          with transaction.atomic():
               if requestUser == postAuthor:
                    return super().update(request, *args, **kwargs)
               else:
                    return Response({'detail': 'You do not have permission to update this post.'}, status=403)
     
   
     @action(detail = True,methods= ['get','post'], url_path='comments',
             serializer_class=CommentSerializer)
     
     def comments(self,request, pk=None):
          if request.method == 'GET':
               post = self.get_object()
               comments = post.comments.all()
               serializer = CommentSerializer(comments, many=True)
               return Response(serializer.data)
          
          #there is no need to make is authinticated because the permission class of the viewset is IsAuthenticatedOrReadOnly
          elif request.method == 'POST':
               post = self.get_object()
               serializer = CommentSerializer(data=request.data)
               if serializer.is_valid():
                    serializer.save(author=request.user, post=post)
                    return Response(serializer.data, status=201)
               else:
                    return Response(serializer.errors, status=400)
    
     #using regix to capture the comment id in the url and then check if the user is the author of the comment before allowing them to update or delete it
     @action(detail=True,methods = ['put','patch','delete'],url_path = 'comments/(?P<comment_id>[^/.]+)',serializer_class=CommentSerializer)
     def comment_detail (self,request,pk=None,comment_id=None):
          if request.method in ['PUT','PATCH']:
               with transaction.atomic():
                    comment = Comment.objects.get(id=comment_id,post_id=pk)
                    if comment.author == request.user:
                         serializer = CommentSerializer(comment,data=request.data, partial=(request.method == 'PATCH'))
                         if serializer.is_valid():
                              serializer.save()
                              return Response(serializer.data)
                         else:
                              return Response(serializer.errors, status=400)
                    else:
                         return Response({'detail': 'You do not have permission to update this comment.'}, status=403)
          elif request.method == 'DELETE':
               with transaction.atomic():
                    comment = Comment.objects.get(id=comment_id,post_id=pk)
                    if comment.author == request.user:
                         comment.delete()
                         return Response(status=204)
                    else:
                         return Response({'detail': 'You do not have permission to delete this comment.'}, status=403)
          
     @action(detail=True, methods=['get','post'], url_path='likes', serializer_class=LikeSerializer)
     def likes(self,request,pk=None):
          post = self.get_object()
          like,created = Like.objects.get_or_create(user=request.user, post=post)
          serializer = LikeSerializer(like)
          if not created:
               like.delete()
               return Response({'detail': 'Post unliked.'}, status=200)
          else:
               return Response({'detail': 'Post liked.'}, status=201)
     
     @method_decorator(cache_page(60*15, key_prefix='*me*'))
     @method_decorator(vary_on_headers('Authorization'))
     @action(detail=False, methods=['get'], url_path='me', serializer_class=PostSerializer)
     def me(self,request):
          my_posts = Post.objects.filter(author=request.user)
          serializer = self.get_serializer(my_posts, many=True)
          return Response(serializer.data)


