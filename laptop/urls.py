from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("shop", views.shop, name="shop"),
    path("inventory/", views.inventory_view, name="inventory"),
    path("services/", views.service, name="services"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("gamingl/", views.gamingl, name="gamingl"),
]