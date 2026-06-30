from django.contrib import admin

from .models import Category, Ingredient, Recipe, RecipePhoto, Step


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


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
    list_display = ('name', 'author', 'difficulty', 'created_at')
    list_filter = ('created_at', 'author', 'difficulty', 'categories')
    search_fields = ('name', 'description')
    filter_horizontal = ('categories',)
    inlines = [IngredientInline, StepInline, RecipePhotoInline]
