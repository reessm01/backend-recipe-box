from recipebox.models import Author, Recipe
from django.contrib.auth.models import User
from django import forms

class AuthorForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'time_rq', 'instructions']

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    is_staff = forms.ChoiceField(widget=forms.RadioSelect, choices=[('1', True), ('2', False)])

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)