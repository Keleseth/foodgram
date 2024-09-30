from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, response, pagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django_filters import rest_framework as filters

from .permissions import RecipePermission
from .models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, FavoriteRecipeSerializer
from users.models import CustomUser


class RecipeFilter(filters.FilterSet):
    
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all().prefetch_related(
        'ingredients',
        'tags',
    ). select_related('author')
    permission_classes = (AllowAny,)
    pagination_class = pagination.PageNumberPagination
    filterset_class = RecipeFilter
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (RecipePermission,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)

    @action(
        ['POST', 'DELETE'],
        detail=True,
        url_path='favorite',
        permission_classes=(IsAuthenticated,),
    )
    def add_favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, id=pk)
        user = self.request.user

        if request.method == 'POST':
            if user.favorited.filter(id=recipe.id).exists():
                return response.Response(
                    {'detail': 'Рецепт уже в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.favorited.add(recipe)
            serializer = FavoriteRecipeSerializer(recipe)
            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            if not user.favorited.filter(id=recipe.id).exists():
                return response.Response(
                    {'detail': 'Рецепт отсутствует в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.favorited.remove(recipe)
            return response.Response(status=status.HTTP_204_NO_CONTENT)