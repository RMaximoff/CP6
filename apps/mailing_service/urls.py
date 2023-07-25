from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static

from .views import HomeView, MailingCreateView, MailingMessageCreate, ClientCreateView, MailingListView, \
    MailingLogListView, ClientListView, ProfileDataView, CabinetView

app_name = 'mailing_service'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cabinet/', CabinetView.as_view(), name="cabinet"),
    path('profile/', ProfileDataView.as_view(), name="profile"),
    path('mailinglist/', MailingListView.as_view(), name="profile_data"),
    path('mailing/', MailingCreateView.as_view(), name='mailing_create'),
    path('client/', ClientCreateView.as_view(), name='client_create'),
    path('mail/', MailingMessageCreate.as_view(), name='mail_create'),


    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('mail/list/', MailingMessageCreate.as_view(), name='mail_list'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
