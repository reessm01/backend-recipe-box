from django.shortcuts import render 

from recipebox.models import Recipe

def index(request, *args, **kwargs):
    page = 'index.html'

    recipes = Recipe.objects.all()

    return render(request, page, {'recipes': recipes})

def author(request, *args, **kwargs):
    page = 'author.html'
    id = int(request.GET.get('id'))
    recipes = Recipe.objects.all().filter(author__id=id)

    return render(request, page, {'recipes': recipes, 'author': recipes[0].author})

def recipe(request, *args, **kwargs):
    page = 'recipe.html'
    uid = int(request.GET.get('id'))
    recipe = Recipe.objects.all().filter(id=uid)
    print(recipe[0].title)
    return render(request, page, {'recipes': recipe, 'author': recipe[0].author})
