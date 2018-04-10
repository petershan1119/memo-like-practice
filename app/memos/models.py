from django.conf import settings
from django.db import models

class Memos(models.Model):
    name_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=230, help_text='메모 내용은 230자 이내로 입력 가능')
    update_date = models.DateTimeField()
    priority = models.BooleanField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return f'{self.title} by {self.name_id}'