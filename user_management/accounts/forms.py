from django import forms
from .models import CustomUser, Post, Category

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

choices = Category.objects.all().values_list('name','name')
choices_list = [ ]

for item in choices:
    choices_list.append(item)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','author','BlogImage','category','summary','content' , 'status')

        widgets =  {
           'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'author': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'','id':'elder', 'type': 'hidden'}),
            'BlogImage': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choices_list,attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=Post.STATUS_CHOICES, attrs={'class': 'form-control'}), 
        }

class EditForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','author','BlogImage','category','summary','content', 'status')

        widgets =  {
           'title': forms.TextInput(attrs={'class': 'form-control'}),
           'author': forms.TextInput(attrs={'class': 'form-control', 'value':'','id':'elder', 'type': 'hidden'}),
            'BlogImage': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choices_list,attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=Post.STATUS_CHOICES, attrs={'class': 'form-control'}), 
        }