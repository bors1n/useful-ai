from django.urls import path
from . import views

urlpatterns = [
    path('favorite/<int:tool_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('<slug:slug>/', views.tool_detail, name='tool_detail'),
] 