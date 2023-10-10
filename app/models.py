from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def is_valid(self):
        return self.expiration_date < timezone.now()

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токени"


class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    orders = models.JSONField()

    class Meta:
        verbose_name = "Клієнт"
        verbose_name_plural = "Клієнти"

