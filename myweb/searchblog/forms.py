# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='A valid email address is required.')
    gender = forms.ChoiceField(choices=CustomUser.GENDER_CHOICES)
    favorite_field = forms.CharField(required=False, help_text='Optional.')
    occupation = forms.CharField(required=False, help_text='Optional.')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'gender', 'favorite_field', 'occupation')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.gender = self.cleaned_data["gender"]
        user.favorite_field = self.cleaned_data["favorite_field"]
        user.occupation = self.cleaned_data["occupation"]
        if commit:
            user.save()
        return user
