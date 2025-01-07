from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import DjTodo
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class DjTodoSerializer(ModelSerializer):
    class Meta:
        model = DjTodo
        fields = '__all__'


class userLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')


    