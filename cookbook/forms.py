from django.forms import CheckboxSelectMultiple, inlineformset_factory, ModelForm

from .models import Ingredient, Recipe, RecipePhoto, Step


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'name',
            'description',
            'categories',
            'cuisine',
            'prep_minutes',
            'cook_minutes',
            'servings',
            'difficulty',
            'calories',
            'protein_g',
            'carbs_g',
            'fat_g',
        ]
        widgets = {
            'categories': CheckboxSelectMultiple,
        }


IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    fields=['quantity', 'unit', 'text', 'order'],
    extra=1,
    can_delete=True,
)

StepFormSet = inlineformset_factory(
    Recipe,
    Step,
    fields=['instruction', 'order'],
    extra=1,
    can_delete=True,
)

PhotoFormSet = inlineformset_factory(
    Recipe,
    RecipePhoto,
    fields=['image', 'caption', 'order'],
    extra=1,
    can_delete=True,
)
