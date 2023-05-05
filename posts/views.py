from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import pagination

from .models import Tweet, TweetImage, Comment
from .permissions import IsAuthorOrAllowAny
from .serializers import TweetSerializer, TweetLikeSerializer, TweetImageSerializer, CommentSerializer, \
    CommentLikeSerializer


class TweetPagination(pagination.PageNumberPagination):
    page_size = 2
    page_query_param = 'p'


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthorOrAllowAny, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body']
    ordering_fields = ['created', ]
    # pagination_class = pagination.LimitOffsetPagination
    pagination_class = TweetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST', ], detail=True, permission_classes=[permissions.IsAuthenticated])
    def like_tweet(self, request, pk=None):
        serializer = TweetLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                tweet_id=pk
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @action(methods=["POST", ], detail=True, permission_classes=[permissions.IsAuthenticated])
    def add_image(self, request, pk=None):
        serializer = TweetImageSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(tweet_id=pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class TweetImageViewSet(viewsets.ModelViewSet):
    queryset = TweetImage.objects.all()
    serializer_class = TweetImageSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthorOrAllowAny, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text', ]
    ordering_fields = ['created', ]
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        tweet_id = self.request.query_params.get('tweet')
        if tweet_id:
            return super().get_queryset().filter(tweet_id=tweet_id)
        else:
            return super().get_queryset()

    @action(methods=['POST', ], detail=True,
            permission_classes=[permissions.IsAuthenticated],
            serializer_class=CommentLikeSerializer)
    def like_comment(self, request, pk=None):
        serializer = CommentLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                user=request.user,
                comment_id=pk
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
