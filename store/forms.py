from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username',
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter email',
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password',
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 4:
            raise forms.ValidationError("Username must be at least 4 characters long.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")

        return email