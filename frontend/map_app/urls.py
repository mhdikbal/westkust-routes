from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("riset/tema/", views.riset_tema, name="riset_tema"),
    path("riset/petunjuk-arsip/", views.riset_petunjuk_arsip, name="riset_petunjuk_arsip"),
    path("riset/jaringan/", views.riset_jaringan, name="riset_jaringan"),
    path("riset/atjeh-dagang/", views.riset_atjeh, name="riset_atjeh"),
    path("riset/pemodelan/", views.riset_pemodelan, name="riset_pemodelan"),
    path("riset/pemodelan/panduan/", views.riset_pemodelan_panduan, name="riset_pemodelan_panduan"),
    path("riset/enclave-1682/", views.riset_enclave_1682, name="riset_enclave_1682"),
    path("linimasa/", views.linimasa, name="linimasa"),
    path("ports/<slug:slug>/", views.port_detail, name="port_detail"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="map_app/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]
