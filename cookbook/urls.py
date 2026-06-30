from django.urls import path

from .views import (
    RecipeCreateView,
    RecipeDeleteView,
    RecipeDetailView,
    RecipeListView,
    RecipeUpdateView,
)

app_name = 'cookbook'

urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path(
        'category/<slug:slug>/',
        RecipeListView.as_view(),
        name='category_detail',
    ),
    path('recipes/new/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
]
