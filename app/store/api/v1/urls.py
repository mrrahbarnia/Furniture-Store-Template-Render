"""
Store API's URL's.
"""
from django.urls import path

from . import apis

app_name = 'store_api'

urlpatterns = [
    path('furniture/', apis.FurnitureApiView.as_view(), name='furniture'),
]
