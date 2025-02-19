from django import forms
from .models import Profile, User, Ingredient


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('picture', 'phone')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomBurgerForm(forms.Form):
    name = forms.CharField(max_length=50, label='Burger Name')

    bun = forms.ModelChoiceField(
        queryset=Ingredient.objects.filter(category='Bun'),
        widget=forms.RadioSelect,
        required=True,
        label='Choose Your Bun'
    )

    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.exclude(category='Bun'),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Choose Your Ingredients'
    )