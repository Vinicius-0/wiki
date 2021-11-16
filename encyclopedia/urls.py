from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:wikiPage>", views.item, name="item"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("new", views.new, name="new"),
    path("edit/<str:wikiPage>", views.edit, name="edit"),
]
