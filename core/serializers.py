from rest_framework import serializers
from .models import User


class UserListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'position', 'is_admin')
        model = User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'position', 'is_admin',
                  'mobile_number', 'address', 'picture', 'date_of_birth', 'skills', 'interest')
        model = User
