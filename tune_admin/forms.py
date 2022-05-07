from django.forms import ModelForm, TextInput, Select
from .models import StateModel


class FullNameForm(ModelForm):
    class Meta:
        model = StateModel  # Your Model Name

    fields = '__all__'

    widgets = {
        'state': TextInput(attrs={'size': '50'}),
    }