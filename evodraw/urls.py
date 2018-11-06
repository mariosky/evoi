
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),

    path('ilike/', views.ilike, name="ilike"),
    path('add_to_collection/', views.add_to_collection, name="add_to_collection"),
    path('remove_from_my_album/', views.remove_from_my_album, name="remove_from_my_album"),
    path('add_rating/', views.rating, name="rating"),
    path('collections/', views.user_collections, name="user_collections"),
    path('album/', views.album, name="album"),
    path('get_my_album/', views.get_my_album, name="get_my_album"),

    path('collection/<str:collection_id>', views.user_collection, name="user_collection"),



    #  path('dashboard/<slug:pop>/', views.dashboard, name="dashboard"),
  #  path('id/<str:individual>', views.details, name="details"),
  #  path('<slug:pop>/next', views.next, name="next"),
  #  path('<slug:pop>/new', views.new, name="new"),
]