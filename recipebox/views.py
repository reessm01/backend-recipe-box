from django.shortcuts import render 

from recipebox.models import Recipe

def index(request, *args, **kwargs):

    index = 'index.html'

    recipes = Recipe.objects.all()

    return render(request, index, {'datas': recipes})