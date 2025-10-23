from django.contrib import admin
from .models import Category, Tag, Event, MediaBlob, Review, ContactMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

class MediaBlobInline(admin.TabularInline):
    model = MediaBlob
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'category', 'city', 'start_datetime', 'status', 'featured')
    list_filter = ('status', 'category', 'city', 'featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [MediaBlobInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'rating', 'created_at')
    list_filter = ('rating',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'email', 'created_at')
