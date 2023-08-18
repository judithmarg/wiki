from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('search', views.search, name='search'),
    path('new_page', views.new_page, name='new_page'),
    path('new_page_save', views.save, name='new_page_save'),
    path('page_edit', views.edit, name='page_edit'),
    path('page_save', views.save_edit, name='page_save'),
    path('random_page', views.random_page, name='random_page'),
    path('wiki/<str:title>', views.entry, name='entry'), 
    path('<str:title>', views.entry, name='entry')   #el orden es importante, se imponen las funciones por delante de otras
]
