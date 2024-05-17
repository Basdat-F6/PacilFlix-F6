from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='Password', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Username',
               'oninvalid': "this.setCustomValidity('Semua field harus diisi')",
               'oninput': "setCustomValidity('')"}))

    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'placeholder': 'Password',
               'oninvalid': "this.setCustomValidity('Semua field harus diisi')",
               'oninput': "setCustomValidity('')"}))

    negara_asal = forms.CharField(label='Negara Asal', max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Negara Asal',
               'oninvalid': "this.setCustomValidity('Semua field harus diisi')",
               'oninput': "setCustomValidity('')"}))
