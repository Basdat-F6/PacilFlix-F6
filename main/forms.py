from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    negara_asal = forms.CharField(label='Negara Asal', max_length=50, help_text='Negara asal Anda')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'negara_asal')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile.objects.create(user=user, country=self.cleaned_data['negara_asal'])
        return user
