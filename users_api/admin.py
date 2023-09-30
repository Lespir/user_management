from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid_ref', 'username', 'email', 'age', 'nationality')
    search_fields = ('uuid_ref', 'username', 'email', 'age', 'nationality')
    list_filter = ('age', 'nationality')
