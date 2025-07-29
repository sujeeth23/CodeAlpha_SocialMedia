from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Email', help_text='')
    first_name = forms.CharField(required=False, label='First Name', help_text='')
    last_name = forms.CharField(required=False, label='Last Name', help_text='')

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text='', 
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        help_text='',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        help_texts = {
            'username': '',
        }