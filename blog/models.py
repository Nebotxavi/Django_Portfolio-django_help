from django.db import models
from users.models import CustomUser
from django.urls import reverse
from django.utils.text import slugify

from taggit.managers import TaggableManager
import datetime

from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )
    slug = models.SlugField(unique=True)
    tags = TaggableManager(blank=True)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

    def partial_content(self):
        if len(self.content) > 320:
            return self.content[:320] + '...'
        else:
            return self.content

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if Post.objects.filter(slug=slugify(self.title)).exists():
            # Generates a unique slug based on the current date
            date_num = datetime.datetime.now()
            self.slug = slugify(self.title) + '-' + \
                str(date_num.strftime("%y%m%d%H%M%S%f"))
        else:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
