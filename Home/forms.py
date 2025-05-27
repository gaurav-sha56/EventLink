from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import  Profile, Virtue, Team





class ProfileForm(forms.ModelForm):
    virtues = forms.ModelMultipleChoiceField(
        queryset=Virtue.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Profile
        fields = ['full_name', 'class_name', 'section', 'net_number', 'about_you', 'profile_picture', 'virtues']



class TeamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']
