from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from accounts.models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required, add email id")
    class Meta:
        model = CustomUser
        fields = ('email','username','password1','password2','official_name','mobile','address','user_type')


class UserAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ('username','password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username,password=password):
                raise forms.ValidationError("Invalid Login")

            #this code prevents users from logging in before admin has approved their accounts
            user = authenticate(username=username,password=password)
            if not user.is_approved:
                raise forms.ValidationError("Admin Approval Pending")


class ProfileEdit(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields = ('email','username','official_name','mobile','address','user_type')
        
    def clean_email(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            try:
                account=CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
            except CustomUser.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use' % email)
        
    def clean_username(self):
        if self.is_valid():
            username=self.cleaned_data['username']
            try:
                account=CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
            except CustomUser.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use' % username)
                