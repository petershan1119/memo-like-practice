from django.conf import settings
from django.db import models
from django.utils import timezone


class Memos(models.Model):
    name_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=50, blank=True)
    text = models.TextField(max_length=230, help_text='메모 내용은 230자 이내로 입력 가능', blank=True)
    update_date = models.DateTimeField(blank=True)
    priority = models.BooleanField(blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)

    @property
    def total_likes(self):
        return self.likes.count()

    def generate(self):
        self.update_date = timezone.now()
        self.save()

    def __str__(self):
        return f'{self.title} by {self.name_id}'