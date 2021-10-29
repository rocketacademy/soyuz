from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Batch, User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")


class AddBatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ["course", "start_date", "number"]
