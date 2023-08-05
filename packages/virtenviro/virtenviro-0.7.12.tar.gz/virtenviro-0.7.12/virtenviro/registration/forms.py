#~*~ coding: utf-8 ~*~
from django import forms


class UserForm(forms.ModelForm):
    firstname = forms.CharField(max_length=30, required=False)
    lastname = forms.CharField(max_length=30, required=False)
    email = forms.CharField(max_length=30)
    pass1 = forms.CharField(widget=forms.PasswordInput, label="Пароль", min_length=6, max_length=30)
    pass2 = forms.CharField(widget=forms.PasswordInput, label="Пароль ещё раз")
    
    def clean_pass2(self):
        if not self.cleaned_data["pass2"] == self.cleaned_data.get("pass1",""):
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data["pass2"]


class UserProfileForm(forms.ModelForm):
    weight = forms.IntegerField( min_value = 10, max_value = 200 )