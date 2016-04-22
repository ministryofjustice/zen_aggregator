from django import forms


class PasswordForm(forms.Form):
    #password = forms.CharField(label='Password', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
