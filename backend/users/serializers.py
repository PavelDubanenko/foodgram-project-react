from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserCreateSerializer(UserCreateSerializer):
    username = serializers.CharField(max_length=150,
                                     min_length=1,
                                     validators=[
                                         UniqueValidator(
                                             queryset=User.objects.all()
                                         )
                                     ]
                                     )
    email = serializers.EmailField(max_length=254,
                                   allow_blank=False,
                                   validators=[
                                       UniqueValidator(
                                           queryset=User.objects.all()
                                       )
                                   ]
                                   )
    first_name = serializers.CharField(max_length=150, min_length=1)
    last_name = serializers.CharField(max_length=150, min_length=1)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Логин "me" нельзя использовать')
        return value
