from django import forms
from .models import Member

class DocumentForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder':'User Name', 'id':'un'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login__input', 'placeholder':'Password', 'id':'pw'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login__input', 'placeholder':'Verify Password', 'id':'pw2'}))
    email = forms.CharField(max_length= 100, widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder':'Email', 'id':'email'}))
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'login__input', 'placeholder':'Name', 'id' :'name'}))
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'login__input', 'id':'dob'}))
    image = forms.FileField()
    class Meta:
        model = Member
        fields = ['username', 'email', 'password', 'name', 'image', 'dob', 'password2']

class UpdateImage(forms.ModelForm):
    mnum = forms.CharField(max_length= 100, widget = forms.HiddenInput())
    image = forms.FileField(widget = forms.FileInput(attrs={'class':'btn btn-primary'}))
    class Meta : 
        model = Member
        fields = ['mnum', 'image']