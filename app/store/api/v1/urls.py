"""
Store API's URL's.
"""
from django.urls import path

from . import apis

app_name = 'store_api'

urlpatterns = [
    path('furniture/', apis.FurnitureApiView.as_view(), name='furniture'),
    path(
        'furniture/<str:slug>/',
        apis.FurnitureDetailApiView.as_view(),
        name='furniture_detail'
    ),
    path(
        'furniture/<str:slug>/rate/',
        apis.RatingFurnitureApiView.as_view(),
        name='furniture_rate'
    )
]
