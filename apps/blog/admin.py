from django.contrib import admin

from apps.blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('create_date', 'title', 'is_published')
