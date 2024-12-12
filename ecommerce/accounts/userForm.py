from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from accounts.models import Account

class RegisterForm(ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
    }))
    repeat_password = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder': 'Repeat password'
    }))
    
    class Meta():
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'repeat_password')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = "Enter Email"
        self.fields['first_name'].widget.attrs['placeholder'] = "Enter FirstName"
        self.fields['last_name'].widget.attrs['placeholder'] = "Enter LastName"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class AccountsForm(ModelForm):
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter phone',
        'class':'form-control',
    }))
    
    class Meta():
        model = Account
        fields = ('phone_number', 'pro_image')

    