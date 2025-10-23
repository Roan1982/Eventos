from django.contrib import admin
from .models import UserProfile, MediaBlob

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'allow_contact')

@admin.register(MediaBlob)
class MediaBlobAdmin(admin.ModelAdmin):
    list_display = ('filename', 'content_type', 'size', 'created_at')
