from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static

from .views import HomeView, MailingCreateView, MailingMessageCreate, ClientCreateView, MailingListView, \
    MailingLogListView, ClientListView, ProfileDataView, CabinetView, MailingUpdateView, ClientUpdateView, \
    MailingMessageUpdateView, MailingDeleteView, ClientDeleteView, MailingMessageDeleteView, MailMessageListView

app_name = 'mailing_service'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cabinet/', cache_page(60)(CabinetView.as_view()), name="cabinet"),
    path('profile/', ProfileDataView.as_view(), name="profile"),

    path('mailing/', MailingCreateView.as_view(), name='mailing_create'),
    path('client/', ClientCreateView.as_view(), name='client_create'),
    path('mail/', MailingMessageCreate.as_view(), name='mail_create'),

    path('mailing-upd/<int:pk>', MailingUpdateView.as_view(), name='mailing_upd'),
    path('client-upd/<int:pk>', ClientUpdateView.as_view(), name='client_upd'),
    path('mail-upd/<int:pk>', MailingMessageUpdateView.as_view(), name='client_upd'),

    path('mailing-list/', MailingListView.as_view(), name="profile_data"),
    path('client-list/', ClientListView.as_view(), name='client_list'),
    path('mail-list/', MailMessageListView.as_view(), name='mail_list'),
    path('mailing-log/', MailingLogListView.as_view(), name='mailing_log'),

    path('mailing-del/<int:pk>', MailingDeleteView.as_view(), name='mailing_del'),
    path('client-del/<int:pk>', ClientDeleteView.as_view(), name='client_del'),
    path('mail-del/<int:pk>', MailingMessageDeleteView.as_view(), name='mail_del'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
