from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Recipes
from rest_framework import generics
from .serializers import RecipesSerializers
from rest_framework.permissions import AllowAny
from .forms import RecipesForm
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import requests


# Create your views here.

class RecipeCreateView(generics.ListCreateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializers
    permission_classes = [AllowAny]


class RecipesDetail(generics.RetrieveAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializers


class RecipesUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializers


class RecipesDelete(generics.DestroyAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializers


class RecipeSearchViewSet(generics.ListAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializers

    def get_queryset(self):
        name = self.kwargs.get('Name')
        return Recipes.objects.filter(Name__icontains=name)

def create_recipe(request):
    if request.method == 'POST':
        form = RecipesForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                api_url = 'http://127.0.0.1:8000/create/'
                data = form.cleaned_data
                response = requests.post(api_url, data=data, files={'Recipe_img': request.FILES['Recipe_img']})
                if response.status_code == 400:
                    messages.success(request, 'Inserted successfully')
                    return redirect('index')
                else:
                    messages.error(request, f'Error: {response.status_code}')
            except requests.RequestException as e:
                messages.error(request, f'Error during API request: {str(e)}')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = RecipesForm()
    return render(request, 'create-recipe.html', {'form': form})

def update_detail(request, id):
    api_url = f'http://127.0.0.1:8000/detail/{id}/'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return render(request, 'recipe_update.html', {'recipe': data})
    else:
        messages.error(request, f'Error fetching recipe details: {response.status_code} - {response.text}')
        return render(request, 'recipe_update.html', {'error': 'Failed to retrieve recipe details'})


def update_recipe(request, id):
    if request.method == 'POST':
        name = request.POST.get('Name')
        prep_time = request.POST.get('Pre_time')
        difficulty = request.POST.get('Difficulty')
        vegetarian = request.POST.get('Vegetarian', 'false') == 'true'
        description = request.POST.get('Description')
        image = request.FILES.get('Recipe_img')

        api_url = f'http://127.0.0.1:8000/update/{id}/'
        data = {
            'Name': name,
            'Pre_time': prep_time,
            'Difficulty': difficulty,
            'Vegetarian': vegetarian,
            'Description': description
        }
        files = {'Recipe_img': image} if image else {}

        response = requests.put(api_url, data=data, files=files)

        # Debugging: Print response content
        print(f'Response Content: {response.content}')

        if response.status_code == 200:
            messages.success(request, 'Recipe updated successfully')
            return redirect('/')
        else:
            messages.error(request, f'Error submitting data to the Rest API: {response.status_code} - {response.text}')

    return render(request, 'recipe_update.html')


def index(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        api_url = f'http://127.0.0.1:8000/search/{search}/'

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
            else:
                data = None
        except requests.RequestException as e:
            data = None
        return render(request, 'index.html', {'data': data})
    else:
        api_url = 'http://127.0.0.1:8000/create/'
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                paginator = Paginator(data, 6)
                try:
                    page = int(request.GET.get('page', 1))
                except ValueError:
                    page = 1

                try:
                    recipes = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    recipes = paginator.page(paginator.num_pages)

                context = {
                    'original_data': data,
                    'recipes': recipes
                }
                return render(request, 'index.html', context)
            else:
                return render(request, 'index.html',
                              {'error_message': f'Error: {response.status_code} - {response.text}'})

        except requests.RequestException as e:
            return render(request, 'index.html', {'error_message': f'Error: {str(e)}'})
    return render(request, 'index.html')


def recipe_fetch(request, id):
    api_url = f'http://127.0.0.1:8000/detail/{id}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        ingredients = data.get('Description', 'No ingredients available')
        return render(request, 'recipe_fetch.html', {'recipes': data, 'ingredients': ingredients})
    return render(request, 'recipe_fetch.html', {'error_message': f'Error: {response.status_code} - {response.text}'})


def recipe_delete(request, id):
    api_url = f'http://127.0.0.1:8000/delete/{id}/'
    response = requests.delete(api_url)
    if response.status_code == 204:  # No Content
        print(f'Item with ID {id} has been deleted')
    else:
        print(f'Failed to delete item. Status code: {response.status_code}')
    return redirect('/')
