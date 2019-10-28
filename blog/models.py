from django.db import models
from users.models import CustomUser
from django.urls import reverse

from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    tags = TaggableManager(blank=True   )

    def __str__(self):
        return self.title

    def partial_content(self):
        if len(self.content) > 150:
            return self.content[:320] + '...'
        else:
            return self.content

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
