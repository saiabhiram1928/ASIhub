from django import forms
from  .models import Room
from  .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  
from django.forms.forms import Form  
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['popularity' , 'participants' , 'host']
        fields = '__all__'
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username' , 'email']
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'profile_pic','bio' ]
class CustomUserCreationForm(UserCreationForm):  
    first_name = forms.CharField(label='First Name', max_length=150)  
    last_name = forms.CharField(label='Last Name', max_length=150)  
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    email = forms.EmailField(label='email')  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            username= self.cleaned_data['username'],  
            first_name=self.cleaned_data['first_name'],  
            last_name =self.cleaned_data['last_name'],  
            email= self.cleaned_data['email'],  
            password=self.cleaned_data['password1']  
        )  
        return user 