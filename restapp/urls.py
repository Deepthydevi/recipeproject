from django.urls import path
from . import views
from .views import *

urlpatterns=[

    path('create/',RecipeCreateView.as_view(),name='create-recipe'),
    path('detail/<int:pk>/',RecipesDetail.as_view(),name='detail'),
    path('update/<int:pk>/',RecipesUpdateView.as_view(),name='update-recipe'),
    path('delete/<int:pk>/',RecipesDelete.as_view(),name='delete-recipe'),
    path('search/<str:Name>/',RecipeSearchViewSet.as_view(),name='search'),

    path('create_recipe/',views.create_recipe,name='create-recipe'),
    path('recipe_fetch/<int:id>/',views.recipe_fetch,name='recipe-fetch'),
    path('update_recipe/<int:id>/',views.update_recipe,name='update_recipe'),
    path('update_detail/<int:id>/',views.update_detail,name='update_detail'),
    path('recipe_delete/<int:id>/',views.recipe_delete,name='recipe_delete'),
    path('',views.index,name='index')


]