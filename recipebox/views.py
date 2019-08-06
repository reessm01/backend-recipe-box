from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login

from recipebox.models import *

from recipebox.forms import *

def index(request, *args, **kwargs):
    page = 'index.html'

    recipes = Recipe.objects.all()

    return render(request, page, {'recipes': recipes})

def register(request, *args, **kwargs):
    if request.method == 'GET':
        page = 'general_form.html'
        title = 'We are excited you are interested in joining:'
        form = RegisterForm()
        return render(request, page, {'form': form, 'title': title})
    else:
        form = RegisterForm(request.POST)
        if User.objects.filter(username=request.POST['username']).count() == 0 and form.is_valid():
            data = form.cleaned_data
            u = User.objects.create_user(
                username=data['username'],
                password=data['password']
            )
            Author.objects.create(
                user=u,
                first_name=data['first_name'],
                last_name=data['last_name'],
            )
            login(request, u)
            return HttpResponseRedirect(reverse('homepage'))

def login_view(request, *args, **kwargs):
    if request.method == 'GET':
        title = 'Welcome back, please login to continue:'
        page = 'general_form.html'
        form = LoginForm()
        return render(request, page, {'form': form, 'title': title})

    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u = authenticate(username=data['username'], password=data['password'])
            if u is not None:
                login(request, u)
            else:
                return HttpResponseRedirect(reverse('login'))
            return HttpResponseRedirect(reverse('homepage'))

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