from django.core.cache import cache

from apps.blog.models import Blog
from config.settings import CACHE_ENABLED


def blog_caching(pk):
    if CACHE_ENABLED:
        key = f'mailing_settings_list_{pk}'
        blog_cache = cache.get(key)
        if blog_cache is None:
            blog_cache = Blog.objects.filter(pk=pk)
            cache.set(key, blog_cache)
    else:
        blog_cache = Blog.objects.filter(pk=pk)
    return blog_cache
