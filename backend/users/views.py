from api.pagination import ApiCustomPagination
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.serializerss import FollowSerializer, UserSerializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from users.models import Subscriptions, User

from .permissions import AuthorOrReadOnly


class UserViewSet(UserViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    pagination_classes = ApiCustomPagination
    add_serializer = FollowSerializer

    @action(methods=('get',), detail=False)
    def subscriptions(self, request):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        pages = self.paginate_queryset(
            User.objects.filter(following__user=self.request.user)
        )
        serializer = FollowSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(AuthorOrReadOnly,)
            )
    def subscribe(self, request, id):
        user = self.request.user
        author = get_object_or_404(self.queryset, id=id)
        serializer = FollowSerializer(author)
        if request.method == 'POST':
            if Subscriptions.objects.filter(
                    user=request.user,
                    author=author).exists():
                raise ValidationError(
                    'Вы уже подписаны на автора')
            if user == author:
                raise ValidationError(
                    'Нельзя подписываться на самого себя!')
            Subscriptions.objects.create(
                user=user,
                author=author)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            in_subscrabed = Subscriptions.objects.filter(
                user=request.user,
                author=author).exists()
            if in_subscrabed is False:
                raise ValidationError("Вы не были подписаны на автора!")
        Subscriptions.objects.filter(
            user=request.user,
            author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)