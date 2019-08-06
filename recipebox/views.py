from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from recipebox.models import *

from recipebox.forms import *


def index(request, *args, **kwargs):
    page = 'index.html'

    recipes = Recipe.objects.all()

    return render(request, page, {'recipes': recipes})

@login_required()
def register(request, *args, **kwargs):
    if request.method == 'GET' and request.user.is_staff:
        page = 'general_form.html'
        title = 'We are excited you are interested in joining:'
        end_point='register'
        form = RegisterForm()
        return render(request, page, {'form': form, 'title': title, 'end_point': end_point})

    elif request.method == 'POST' and request.user.is_staff:
        form = RegisterForm(request.POST)
        if User.objects.filter(username=request.POST['username']).count() == 0 and form.is_valid():
            data = form.cleaned_data
            staff = True if data['is_staff'] == 1 else False
            u = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                is_staff=staff
            )
            Author.objects.create(
                user=u,
                first_name=data['first_name'],
                last_name=data['last_name'],
            )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        page = 'general_form.html'
        title = 'ERROR:'
        message = 'Sorry, you must be a staff member to view this page.'
        form = RegisterForm()
        return render(request, page, {'title': title, 'message': message, 'disabled': True})


def login_view(request, *args, **kwargs):
    if request.method == 'GET' and str(request.user) == 'AnonymousUser':
        title = 'Welcome back, please login to continue:'
        page = 'general_form.html'
        end_point='login'
        form = LoginForm()
        return render(request, page, {'form': form, 'title': title, 'end_point': end_point})

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u = authenticate(
                username=data['username'], password=data['password'])
            if u is not None:
                login(request, u)
            else:
                title = 'Welcome back, please login to continue:'
                page = 'general_form.html'
                message = 'Username or password is incorrect.'
                end_point='login'
                form = LoginForm()
                return render(request, page, {'form': form, 'title': title, 'end_point': end_point, 'message': message})

            destination = request.GET.get('next')
            if destination:
                return HttpResponseRedirect(destination)
            return HttpResponseRedirect(reverse('homepage'))
    else:
        return HttpResponseRedirect(reverse('homepage'))


def author(request, *args, **kwargs):
    page = 'author.html'
    id = int(request.GET.get('id'))
    recipes = Recipe.objects.all().filter(author__id=id)
    formal_name = recipes[0].author.first_name + \
        ' ' + recipes[0].author.last_name

    return render(request, page, {'recipes': recipes, 'author': formal_name})


def recipe(request, *args, **kwargs):
    page = 'recipe.html'
    uid = int(request.GET.get('id'))
    recipe = Recipe.objects.all().filter(id=uid)
    return render(request, page, {'recipes': recipe, 'author': recipe[0].author})


@login_required()
def addrecipe(request, *args, **kwargs):
    if request.method == 'GET':
        page = 'create_recipe.html'
        form = RecipeForm()
        return render(request, page, {'form': form})
    else:
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            u = request.user
            Recipe.objects.create(
                title=data['title'],
                description=data['description'],
                time_rq=data['time_rq'],
                instructions=data['instructions'],
                author=Author.objects.get(user=u)
            )
        return HttpResponseRedirect(reverse('homepage'))


def logout_user(request, *args, **kwargs):
    res = HttpResponseRedirect(reverse('homepage'))
    res.delete_cookie('sessionid')
    return res
