from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Batch, User


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # email is uneditable because it must be the
        # same as the hubspot link
        self.fields["email"].widget = forms.HiddenInput()

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email already exists")

        return email


class AddUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        del self.fields["password2"]
        self.fields["password1"].help_text = None

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email already exists")

        return email


class AddBatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Batch
        fields = ["course", "start_date", "number", "max_capacity", "gcal_link"]
        widgets = {"start_date": forms.DateInput(attrs={"type": "date"})}
