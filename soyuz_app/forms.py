from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Batch, User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class AddBatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['course_id', 'start_date', 'number']
