from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static

from .views import HomeView, MailingCreate, MailingMessageCreate, ClientCreateView, MailingListView, \
    MailingStatusUpdateView, MailingLogDetailView

app_name = 'mailing_service'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cabinet/', MailingListView.as_view(), name="cabinet"),
    path('mailing/', MailingCreate.as_view(), name='mailing_create'),
    path('mail/', MailingMessageCreate.as_view(), name='mail_create'),
    path('client/', ClientCreateView.as_view(), name='client_create'),
    path('update_status/<int:pk>/', MailingStatusUpdateView.as_view(), name='update_status'),
    path('mailing_log/<int:pk>/', MailingLogDetailView.as_view(), name='mailing_log_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
