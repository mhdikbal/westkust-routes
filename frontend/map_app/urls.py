from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("riset/tema/", views.riset_tema, name="riset_tema"),
    path("riset/petunjuk-arsip/", views.riset_petunjuk_arsip, name="riset_petunjuk_arsip"),
    path("riset/jaringan/", views.riset_jaringan, name="riset_jaringan"),
    path("riset/atjeh-dagang/", views.riset_atjeh, name="riset_atjeh"),
    path("riset/pemodelan/", views.riset_pemodelan, name="riset_pemodelan"),
    path("linimasa/", views.linimasa, name="linimasa"),
    path("ports/<slug:slug>/", views.port_detail, name="port_detail"),
]
