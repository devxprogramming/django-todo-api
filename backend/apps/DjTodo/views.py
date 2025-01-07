from django.shortcuts import render, redirect
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import DjTodo
from .serializer import DjTodoSerializer, userLoginSerializer
from rest_framework.viewsets import ModelViewSet
from typing import Any

class todoView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DjTodo.objects.all()
    serializer_class = DjTodoSerializer
    http_method_names = ['get', 'post', 'delete']
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
    

    def get_todos(self, request):
        todos = DjTodo.objects.all().filter(user=request.user)
        serializer = DjTodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create_todo(self, request, *args, **kwargs):
        serializer = DjTodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete_todo(self, request, pk, *args, **kwargs):
        try:
            get_the_todo = DjTodo.objects.get(pk=pk)
            if get_the_todo.user == request.user:
                get_the_todo.delete()
                return Response({"message": "Todo deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You are not allowed to delete this todo"}, status=status.HTTP_400_BAD_REQUEST)
        except DjTodo.DoesNotExist or DjTodo.MultipleObjectsReturned:
            return Response({"error": "Todo does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_specific_todo(self, request, pk, *args, **kwargs):
        try:
            get_the_todo = DjTodo.objects.get(pk=pk)
            if get_the_todo.user == request.user:
                serializer = DjTodoSerializer(get_the_todo)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else: 
                return Response({"error": "You are not allowed to view this todo"}, status=status.HTTP_400_BAD_REQUEST)
        except DjTodo.DoesNotExist or DjTodo.MultipleObjectsReturned:
            return Response({"error": "Todo does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        