from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Batch, User


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # email is uneditable because it must be the
        # same as the hubspot link
        self.fields["email"].widget.attrs["readonly"] = True

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is not unique")


class AddBatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Batch
        fields = ["course", "start_date", "number"]
        widgets = {"start_date": forms.DateInput(attrs={"type": "date"})}
