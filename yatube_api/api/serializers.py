from email.policy import default
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('id',)


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        read_only=True,
        # slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    # @api_view(['POST'])
    def validate_following(self, data):
        if data['following'] is None:
            raise serializers.ValidationError(
                'Отсутствует following.'
            )
        if self.context.get('request').user == data['following']:
            raise serializers.VaildationError(
                'Подписка на себя невозможна.'
            )
        return data

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user','following')
            )
        ]
