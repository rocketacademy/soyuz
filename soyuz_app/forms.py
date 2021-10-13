from django import forms
from .models import Batch


# class RegistrationForm(forms.Form):
#     github_username = forms.CharField(label='Github username')


class AddBatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['course_id', 'start_date', 'number']


# class RegisterForm(UserCreationForm):

#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ['email', 'username', 'password1', 'password2']
