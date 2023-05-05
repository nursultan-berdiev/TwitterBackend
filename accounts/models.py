from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_avatar = models.ImageField(default='profile/default-avatar.png', upload_to='profile')

    def __str__(self):
        return self.username


# class Table(models.Model):
#     small_serial = models.SmallAutoField(primary_key=True)
#     # serial = models.AutoField()
#     # big_serial = models.BigAutoField()
#     small_integer = models.SmallIntegerField()
#     big_integer = models.BigIntegerField()
#     numeric = models.FloatField()
#     models.CharField()
