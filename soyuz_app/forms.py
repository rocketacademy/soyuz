from django import forms
from .models import Batch, User


class RegistrationForm(forms.Form):
    github_username = forms.CharField(label='Github username')


class AddBatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['course_id', 'start_date', 'number']
