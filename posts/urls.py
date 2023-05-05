from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('tweet', views.TweetViewSet)
router.register('tweet_image', views.TweetImageViewSet)
router.register('comment', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('tweet/<int:pk>/like', views.TweetLikeDislikeAPIView.as_view())
]
