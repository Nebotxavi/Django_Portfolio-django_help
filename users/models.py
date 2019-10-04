from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(
        default='new_default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} profile'

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
