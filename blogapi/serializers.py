from restframework import serializers
from .models import Post, Comment, Like, User

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'image']

class LikeSerializer (serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']

    
class CommentSerializer (serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

class PostSerializer (serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    total_likes = serializers.IntegerField (source= 'likes.count', read_only=True)
    total_comments = serializers.IntegerField (source= 'comments.count', read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'comments', 'total_likes', 'total_comments']
