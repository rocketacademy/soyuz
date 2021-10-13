from django import forms
from .models import Batch, User

from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class AddBatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['course_id', 'start_date', 'number']
