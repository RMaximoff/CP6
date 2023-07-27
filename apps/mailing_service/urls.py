from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static

from .views import HomeView, MailingCreateView, MailingMessageCreate, ClientCreateView, MailingListView, \
    MailingLogListView, ClientListView, ProfileDataView, CabinetView, MailingUpdateView, ClientUpdateView, \
    MailingMessageUpdateView, MailingDeleteView, ClientDeleteView, MailingMessageDeleteView, MailMessageListView, \
    ModeratorViews, MailingStatusUpdateView

app_name = 'mailing_service'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cabinet/', CabinetView.as_view(), name="cabinet"),
    path('profile/', ProfileDataView.as_view(), name="profile"),
    path('moderka/', ModeratorViews.as_view(), name="moderators"),

    path('mailing/', MailingCreateView.as_view(), name='mailing_create'),
    path('client/', ClientCreateView.as_view(), name='client_create'),
    path('mail/', MailingMessageCreate.as_view(), name='mail_create'),

    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_upd'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_upd'),
    path('mail/<int:pk>/update/', MailingMessageUpdateView.as_view(), name='client_upd'),

    path('mailing-list/', MailingListView.as_view(), name="profile_data"),
    path('client-list/', ClientListView.as_view(), name='client_list'),
    path('mail-list/', MailMessageListView.as_view(), name='mail_list'),
    path('mailing-log/<int:pk>', MailingLogListView.as_view(), name='mailing_log'),

    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_del'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_del'),
    path('mail/<int:pk>/delete/', MailingMessageDeleteView.as_view(), name='mail_del'),
    path('update_status/<int:pk>/', MailingStatusUpdateView.as_view(), name='update_status'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
