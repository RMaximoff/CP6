from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, TemplateView, DeleteView
from apps.blog.models import Blog
from apps.mailing_service.forms import MailingSettingsForm, MailingMessageForm, ClientForm, MailingFilterForm
from apps.mailing_service.models import MailingSettings, Client, MailingMessage, MailingLog


# create ----------------------------------------------------------------


class MailingCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:cabinet')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:cabinet')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingMessageCreate(CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:cabinet')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# list ----------------------------------------------------------------


class MailingListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = 'mailing_service/mailingsettings_list.html'
    context_object_name = 'mailing_list'

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators'):
            queryset = MailingSettings.objects.all()
        else:
            queryset = MailingSettings.objects.filter(owner_id=self.request.user.pk)

        owner_id = self.request.user.pk
        state = self.request.GET.get('status')
        if self.request.GET.get('status'):
            queryset = MailingSettings.objects.filter(owner_id=owner_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = MailingFilterForm(self.request.GET)
        return context


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing_service/client_list.html'
    context_object_name = 'client_list'

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators'):
            queryset = Client.objects.all()
        else:
            queryset = Client.objects.filter(owner_id=self.request.user.pk)
        return queryset


class MailMessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage
    template_name = 'mailing_service/mail_list.html'
    context_object_name = 'mail_list'

    def get_queryset(self):
        if self.request.user.groups.filter(name='moderators'):
            queryset = MailingMessage.objects.all()
        else:
            queryset = MailingMessage.objects.filter(owner_id=self.request.user.pk)
        return queryset


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog
    template_name = 'mailing_service/mailinglog_list.html'
    context_object_name = 'mailing_log_list'

    def get_queryset(self):
        mailing_pk = self.kwargs.get('mailing_pk')
        mailing_settings = get_object_or_404(MailingSettings, pk=mailing_pk)
        queryset = MailingLog.objects.filter(mailing=mailing_settings)
        return queryset


# update ----------------------------------------------------------------


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:cabinet')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().owner


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().owner


class MailingMessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    template_name = 'mailing_service/mailing_form.html'
    success_url = reverse_lazy('mailing_service:mail_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().owner

# delete ----------------------------------------------------------------


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingSettings
    template_name = 'mailing_service/confirm_delete.html'
    success_url = reverse_lazy('mailing_service:cabinet')

    def test_func(self):
        return self.request.user == self.get_object().owner


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'mailing_service/confirm_delete.html'
    success_url = reverse_lazy('mailing_service:client_list')

    def test_func(self):
        return self.request.user == self.get_object().owner


class MailingMessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingSettings
    template_name = 'mailing_service/confirm_delete.html'
    success_url = reverse_lazy('mailing_service:mail_list')

    def test_func(self):
        return self.request.user == self.get_object().owner


# other -------------------------------------------------------------------------


class HomeView(TemplateView):
    template_name = 'mailing_service/base.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['count_mail_all'] = MailingSettings.objects.all().count()
        context_data['count_mail_active'] = MailingSettings.objects.filter(mailing_status__in=['started']).count()
        context_data['count_clients'] = Client.objects.distinct().count()
        context_data['blog'] = Blog.objects.filter(is_published=True).order_by('?')[:3]
        context_data['user'] = self.request.user
        return context_data


class ProfileDataView(TemplateView):
    template_name = 'mailing_service/cabinet.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        owner_id = self.request.user.pk
        context_data['count_mailing_all'] = MailingSettings.objects.filter(owner_id=owner_id).count()
        context_data['count_mailing_active'] = MailingSettings.objects.filter(mailing_status__in=['started'],
                                                                              owner_id=owner_id).count()
        context_data['count_mail_massage'] = MailingMessage.objects.filter(owner_id=owner_id).count()
        context_data['count_clients'] = Client.objects.filter(owner_id=owner_id).count()
        return context_data


class CabinetView(TemplateView):
    template_name = 'mailing_service/cabinet.html'

    def get(self, request, *args, **kwargs):

        profile_data_view = ProfileDataView()
        profile_data_view.request = request
        profile_context = profile_data_view.get_context_data(**kwargs)

        mailing_list_view = MailingListView()
        mailing_list_view.request = request
        queryset = mailing_list_view.get_queryset()
        count_mailing_all = queryset.count()
        mailing_context = {
            'mailing_list': queryset,
            'count_mailing_all': count_mailing_all,
        }

        combined_context = {**profile_context, **mailing_context}
        combined_context['filter_form'] = MailingFilterForm(request.GET)

        return render(request, self.template_name, combined_context)


class ModeratorViews(UserPassesTestMixin, TemplateView):
    template_name = 'mailing_service/moderators.html'

    def test_func(self):
        return self.request.user.groups.filter(name='moderators').exists()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        return context_data


class MailingStatusUpdateView(View):
    def post(self, request, *args, **kwargs):
        mailing_id = kwargs['pk']
        new_status = request.POST.get('new_status')
        mailing = MailingSettings.objects.get(pk=mailing_id)
        mailing.mailing_status = new_status
        mailing.save()

        return redirect('mailing_service:cabinet')


