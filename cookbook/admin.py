from django.contrib import admin

from .models import Ingredient, Recipe, RecipePhoto, Step


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class StepInline(admin.TabularInline):
    model = Step
    extra = 1


class RecipePhotoInline(admin.TabularInline):
    model = RecipePhoto
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('name', 'description')
    inlines = [IngredientInline, StepInline, RecipePhotoInline]
