from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from django.db.models import Q
from django.shortcuts import get_object_or_404

from .forms import (
    IngredientFormSet,
    PhotoFormSet,
    RecipeForm,
    StepFormSet,
)
from .models import Category, Recipe


class RecipeListView(ListView):
    model = Recipe
    template_name = 'cookbook/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12

    def get_category(self):
        slug = self.kwargs.get('slug')
        if slug:
            return get_object_or_404(Category, slug=slug)
        return None

    def get_queryset(self):
        qs = (
            Recipe.objects
            .select_related('author')
            .prefetch_related('photos', 'categories')
        )
        category = self.get_category()
        if category:
            qs = qs.filter(categories=category)
        query = self.request.GET.get('q', '').strip()
        if query:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(cuisine__icontains=query)
                | Q(ingredients__text__icontains=query)
            ).distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '').strip()
        ctx['category'] = self.get_category()
        ctx['categories'] = Category.objects.all()
        return ctx


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'cookbook/recipe_detail.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        return (
            Recipe.objects
            .select_related('author')
            .prefetch_related('ingredients', 'steps', 'photos')
        )


class _RecipeFormsetMixin:
    def get_formsets(self, instance=None):
        post = self.request.POST or None
        files = self.request.FILES or None
        return {
            'ingredient_formset': IngredientFormSet(
                post, files, instance=instance, prefix='ingredients'
            ),
            'step_formset': StepFormSet(
                post, files, instance=instance, prefix='steps'
            ),
            'photo_formset': PhotoFormSet(
                post, files, instance=instance, prefix='photos'
            ),
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        instance = getattr(self, 'object', None)
        if 'ingredient_formset' not in ctx:
            ctx.update(self.get_formsets(instance=instance))
        return ctx

    def form_valid(self, form):
        formsets = self.get_formsets(instance=form.instance)
        if not all(fs.is_valid() for fs in formsets.values()):
            return self.render_to_response(
                self.get_context_data(form=form, **formsets)
            )

        with transaction.atomic():
            self.object = self._save_parent(form)
            for fs in formsets.values():
                fs.instance = self.object
                fs.save()

        return super().form_valid(form)

    def _save_parent(self, form):
        return form.save()


class RecipeCreateView(LoginRequiredMixin, _RecipeFormsetMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'cookbook/recipe_form.html'

    def _save_parent(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.save()
        return recipe


class RecipeUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, _RecipeFormsetMixin, UpdateView
):
    model = Recipe
    form_class = RecipeForm
    template_name = 'cookbook/recipe_form.html'

    def test_func(self):
        return self.get_object().author_id == self.request.user.id


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'cookbook/recipe_confirm_delete.html'
    success_url = reverse_lazy('cookbook:recipe_list')

    def test_func(self):
        return self.get_object().author_id == self.request.user.id
