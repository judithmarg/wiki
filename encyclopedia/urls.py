from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search', views.search, name='search'),
    path('new_page', views.new_page, name='new_page'),
    path('new_page_save', views.save, name='new_page_save'),
    path('<str:title>', views.entry, name='entry')   #el orden es importante, se imponen las funciones por delante de otras
]
