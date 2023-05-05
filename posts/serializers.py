from rest_framework import serializers
from django.db.utils import IntegrityError

from .models import Tweet, TweetLike, TweetImage, Comment, CommentLike


class TweetImageListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        result = []
        for data in validated_data:
            result.append(TweetImage.objects.create(**data))
        return result


class TweetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetImage
        fields = "__all__"
        list_serializer_class = TweetImageListSerializer


class TweetSerializer(serializers.ModelSerializer):
    likes_dislikes = serializers.ReadOnlyField(source='get_likes_dislikes')
    images = serializers.ReadOnlyField(source='get_images')

    class Meta:
        model = Tweet
        fields = "__all__"
        read_only_fields = ['user', ]


class TweetLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetLike
        fields = "__all__"
        read_only_fields = ['user', 'tweet', ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            tweet_like = TweetLike.objects.get(
                user=validated_data['user'],
                tweet_id=validated_data['tweet_id']
            )
            if tweet_like.is_like != validated_data['is_like']:
                tweet_like.is_like = not tweet_like.is_like
                tweet_like.save()
            return tweet_like


class CommentSerializer(serializers.ModelSerializer):
    marks = serializers.ReadOnlyField(source='get_mark')
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', ]


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"
        read_only_fields = ['user', 'comment', ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            comm_like = CommentLike.objects.get(
                user=validated_data['user'],
                comment_id=validated_data['comment_id']
            )
            if comm_like.mark != validated_data['mark']:
                comm_like.mark = validated_data['mark']
                comm_like.save()
            return comm_like

