from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView, TemplateView, DeleteView
from apps.blog.models import Blog
from apps.mailing_service.forms import MailingSettingsForm, MailingMessageForm, ClientForm, MailingFilterForm
from apps.mailing_service.models import MailingSettings, Client, MailingMessage, MailingLog


class HomeView(TemplateView):
    template_name = 'mailing_service/base.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['count_mail_all'] = MailingSettings.objects.all().count()
        context_data['count_mail_active'] = MailingSettings.objects.filter(mailing_status__in=['started']).count()
        context_data['count_clients'] = Client.objects.distinct().count()
        context_data['blog'] = Blog.objects.filter(is_published=True).order_by('?')[:3]
        return context_data


class MailingCreate(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing_service:cabinet')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingMessageCreate(CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing_service:cabinet')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing_service:cabinet')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = MailingSettings
    template_name = 'mailing_service/mailingsettings_list.html'
    context_object_name = 'mailing_list'

    def get_queryset(self):
        queryset = MailingSettings.objects.filter(owner_id=self.request.user.pk)
        state = self.request.GET.get('status')
        if self.request.GET.get('status'):
            queryset = queryset.filter(mailing_status=state)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = MailingFilterForm(self.request.GET)
        return context


class MailingStatusUpdateView(View):
    def post(self, request, *args, **kwargs):
        mailing_id = kwargs['pk']
        new_status = request.POST.get('new_status')
        mailing = MailingSettings.objects.get(pk=mailing_id)
        mailing.mailing_status = new_status
        mailing.save()

        return redirect('mailing_service:cabinet')


class MailingLogDetailView(DetailView):
    model = MailingLog
    template_name = 'mailing_service/mailinglog_detail.html'
    context_object_name = 'mailing_log'





