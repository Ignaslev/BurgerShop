from django import forms
from .models import Profile, User


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture', 'phone')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)