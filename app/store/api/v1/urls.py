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
    ),
    path(
        'company/active/',
        apis.ActiveCompaniesApiView.as_view(),
        name='active_company'
    ),
    path('company/all/', apis.CompanyApiView.as_view(), name='company'),
    path(
        'company/<str:slug>/activate/',
        apis.ActivateCompanyApiView.as_view(),
        name='activate_company'
    ),
    path(
        'company/<str:slug>/deactivate/',
        apis.DeactivateCompanyApiView.as_view(),
        name='deactivate_company'
    )
]
