from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    
    class Meta:
        model=User
        fields = ('username', 'first_name', 'email')
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match")
        return cd['password2']
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('User', 'balance', 'alive')
        # fields = ('date_of_birth', 'photo')


class TransferForm(forms.Form):
    profiles = Profile.objects.filter(user__is_staff=False).filter(alive=True)
    choices = [(prof.user.id, prof.user.username) for prof in profiles]
    Player = forms.ChoiceField(choices=choices)
    amount = forms.FloatField()

class KillerForm(forms.Form):
    profiles = Profile.objects.filter(user__is_staff=False).filter(alive=True)
    choices = [(prof.user.id, prof.user.username) for prof in profiles]
    Player = forms.ChoiceField(choices=choices)