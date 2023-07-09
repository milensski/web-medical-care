from django.contrib import admin
from django.contrib.auth import get_user_model

from web.app_auth.models import Profile

# Register your models here.
UserModel = get_user_model()


@admin.register(UserModel)
class UsersAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

