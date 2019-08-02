from django.shortcuts import render, HttpResponseRedirect, reverse

from recipebox.models import Recipe, Author

from recipebox.forms import RecipeForm, AuthorForm

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
    return render(request, page, {'recipes': recipe, 'author': recipe[0].author})

def addauthor(request, *args, **kwargs):
    if request.method == 'GET':
        page = 'create_author.html'
        form = AuthorForm()
        return render(request, page, {'form': form})
    else:
        form = AuthorForm(request.POST)
        if Author.objects.filter(name=request.POST['name']).count() == 0 and form.is_valid():
            data = form.cleaned_data
            Author.objects.create(
                name=data['name'],
                bio=data['bio']
            )
        return HttpResponseRedirect(reverse('homepage'))

def addrecipe(request, *args, **kwargs):
    if request.method == 'GET':
        page = 'create_recipe.html'
        form = RecipeForm()
        return render(request, page, {'form': form})
    else:
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data['title'],
                description=data['description'],
                time_rq=data['time_rq'],
                instructions=data['instructions'],
                author=Author.objects.get(name=data['author'])
            )
        return HttpResponseRedirect(reverse('homepage'))