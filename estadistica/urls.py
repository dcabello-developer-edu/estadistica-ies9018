from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/calcular/", views.api_calcular, name="api_calcular"),
]
