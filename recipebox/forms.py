from recipebox.models import Author, Recipe
from django import forms

class AuthorForm(forms.Form):
    name = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'time_rq', 'instructions', 'author']