from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = get_user_model()
    fieldsets = UserAdmin.fieldsets + (None, {"fields": ("wins", "draws", "loses")})
    add_fieldsets = UserAdmin.add_fieldsets
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = [
        "username",
        "email",
        "wins",
        "draws",
        "loses",
    ]


admin.site.register(get_user_model(), CustomUserAdmin)
