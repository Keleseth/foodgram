from rest_framework import response, status


def check_and_add(request, object, serializer_class):
    user = request.user
    serializer = serializer_class(
        data={
            'user': user.id,
            'recipe': object.id
        },
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return response.Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


def check_and_delete_from_favorite(request, object):
    user = request.user
    if not user.favorited.filter(id=object.id).exists():
        return response.Response(
            {'detail': 'Рецепт отсутствует в избранном.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    user.favorited.remove(object)
    return response.Response(status=status.HTTP_204_NO_CONTENT)


def check_and_add_to_cart(request, object, serializer_class):
    user = request.user
    serializer = serializer_class(
        data={
            'user': user.id,
            'recipe': object.id
        },
        context={'request': request}
    )
    return response.Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


def check_and_delete_from_cart(request, object):
    user = request.user
    if not user.recipes_in_cart.filter(id=object.id).exists():
        return response.Response(
            {'detail': 'Рецепт отсутствует в корзине.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    user.recipes_in_cart.remove(object)
    return response.Response(status=status.HTTP_204_NO_CONTENT)
