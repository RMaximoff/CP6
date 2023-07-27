from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'

urlpatterns = [
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/create/', views.PostCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/', views.PostView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/update/', views.PostUpdateView.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete/', cache_page(60)(views.PostDeleteView.as_view()), name='blog_delete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

