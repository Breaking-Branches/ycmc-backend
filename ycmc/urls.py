from django.urls import path
from . import views

urlpatterns = [
    path('files', views.HomeView.as_view()),
    path('detect/<str:pid>', views.DetectHome.as_view()),
]
