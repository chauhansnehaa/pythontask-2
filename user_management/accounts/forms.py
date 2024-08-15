from django import forms
from .models import CustomUser

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=[('Doctor', 'Doctor'), ('Patient', 'Patient')])


    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_picture', 'username', 'email', 'password', 'address_line1', 'city', 'state', 'pincode', 'user_type']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=[('Doctor', 'Doctor'), ('Patient', 'Patient')], required=True)

