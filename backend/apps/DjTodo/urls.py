from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()


router.register(r'create', views.todoView, basename='create')
router.register(r'delete/<int:pk>', views.todoView, basename='delete')
router.register(r'all-todos', views.todoView, basename='all-todos')
router.register(r'get-todo/<int:pk>', views.todoView, basename='get-todo')


urlpatterns = [
    path('create/', views.todoView.as_view({'post':'create_todo'}), name='create'),
    path('delete/<int:pk>', views.todoView.as_view({'get':'get_specific_todo','delete':'delete_todo'}), name='delete'),
    path('all-todos/', views.todoView.as_view({'get':'get_todos'}), name='all-todos'),
    path('get-todo/<int:pk>', views.todoView.as_view({'get':'get_specific_todo'}), name='get-todo'),
]


urlpatterns += router.urls