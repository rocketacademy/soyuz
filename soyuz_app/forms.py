from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Batch, User


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class AddBatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Batch
        fields = ["course", "start_date", "number"]
        widgets = {"start_date": forms.DateInput(attrs={"type": "date"})}
