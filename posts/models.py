from django.db import models

from accounts.models import User

COMMENT_CHOISES = [
    ('like', 'like'),
    ('dislike', 'dislike')
]


class Tweet(models.Model):
    title = models.CharField(max_length=240)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tweets')

    def get_likes_dislikes(self):
        likes_dislikes = TweetLike.objects.filter(tweet=self)
        likes = likes_dislikes.filter(is_like=True).count()
        dislikes = likes_dislikes.filter(is_like=False).count()
        return {
            'likes': likes,
            'dislikes': dislikes
        }

    def get_images(self):
        return TweetImage.objects.filter(tweet=self).values()

    def __str__(self):
        return self.title


class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    is_like = models.BooleanField()

    class Meta:
        unique_together = ['user', 'tweet']

    def __str__(self):
        return f'{self.user} - {self.tweet} : {self.is_like}'


def tweet_image_store(instance, filename):
    last_image = TweetImage.objects.all().order_by("-id").first()
    if last_image:
        next_id = last_image.id + 1
    else:
        next_id = 1
    file_ext = filename.split('.')[-1]
    new_file_name = f'{instance.tweet.user.username}_{next_id}.{file_ext}'
    return f'tweet_images/tweet_{instance.tweet.id}/{new_file_name}'


class TweetImage(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=tweet_image_store)

    def __str__(self):
        return f'image for {self.tweet.id}'


class Comment(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_mark(self):
        result = {}
        for mark_name in COMMENT_CHOISES:
            result[mark_name[1]] = CommentLike.objects.filter(
                mark=mark_name[0],
                comment=self).count()
        return result

    def __str__(self):
        return f'{self.text} - {self.tweet}'


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mark = models.CharField(choices=COMMENT_CHOISES, max_length=10)
    liked_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'comment']

    def __str__(self):
        return f'{self.comment.id} {self.mark}'
