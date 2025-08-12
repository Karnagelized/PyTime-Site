
from django.contrib import admin
from .models import CustomUser, ProfileAvatarModel
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin


# Регистрируем CustomUser в Админке
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'aboutMe', 'avatar')
    list_display_links = ('username',)


@admin.register(ProfileAvatarModel)
class ProfileAvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'avatar')
    list_display_links = ('id',)

    class Meta:
        model = ProfileAvatarModel
