from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models


class OwnUser(User):

    send_emails = models.BooleanField()


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        if commit:
            user.save()

        return user


class OwnUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    send_emails = forms.BooleanField(required=False)

    class Meta:
        model = OwnUser
        fields = ("username", "email", "send_emails", "password1", "password2")

    def save(self, commit=True):
        user = super(OwnUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.send_emails = self.cleaned_data["send_emails"]

        if commit:
            user.save()

        return user


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username",)


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ("user_dp",)

