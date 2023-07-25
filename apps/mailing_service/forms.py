from datetime import datetime

from django import forms
from django.forms import DateTimeInput, DateInput


from apps.mailing_service.models import MailingSettings, MailingMessage, Client


class FormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control-10'


class MailingMessageForm(FormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = '__all__'
        exclude = ('owner',)


class MailingSettingsForm(FormMixin, forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(queryset=Client.objects.all(), widget=forms.CheckboxSelectMultiple,
                                             label='Клиенты')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mailing_start_time'].widget = DateInput(attrs={'type': 'datetime-local'})
        self.fields['mailing_end_time'].widget = DateInput(attrs={'type': 'datetime-local'})

    class Meta:
        model = MailingSettings
        fields = '__all__'
        exclude = ('mailing_status', 'owner',)


class ClientForm(FormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('owner',)


class MailingFilterForm(forms.Form):
    status_choices = MailingSettings.STATUS_CHOICES

    status = forms.ChoiceField(choices=[('', 'Все')] + list(status_choices),
                               required=False,
                               widget=forms.Select(attrs={'id': 'status'}))
