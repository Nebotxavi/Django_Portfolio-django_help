from django.contrib import admin
from .models import Post
from users.forms import CustomUserCreationForm
from users.models import CustomUser, Profile
from comments.models import Comment
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    form = CustomUserCreationForm
    model = CustomUser
    list_display = ['username', 'email']


admin.site.register(Post)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Comment)
