from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("riset/tema/", views.riset_tema, name="riset_tema"),
    path("ports/<slug:slug>/", views.port_detail, name="port_detail"),
]
