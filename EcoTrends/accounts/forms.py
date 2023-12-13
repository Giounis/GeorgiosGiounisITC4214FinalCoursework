from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm,PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser
class CustomUserCreationForm(UserCreationForm):#Form for the user creation, mostly sign up 
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class CustomUserChangeForm(UserChangeForm):#username change
    class Meta:
        model = get_user_model()
        fields = ('username',)
class CustomPasswordChangeForm(PasswordChangeForm):#password change
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )