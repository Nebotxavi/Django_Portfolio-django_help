from django.db import models
from users.models import CustomUser
# from blog.models import Post

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    # post = models.ForeignKey(
    #     Post, on_delete=models.CASCADE, related_name='comments')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)
