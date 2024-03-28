"""
Store API's URL's.
"""
from django.urls import path

from . import apis

app_name = 'store_api'

urlpatterns = [
    # ============= Furniture URL's ============= #
    path(
        'furniture/active/',
        apis.ActiveFurnitureApiView.as_view(),
        name='active_furniture'
    ),
    path(
        'furniture/',
        apis.FurnitureApiView.as_view(),
        name='furniture'
    ),
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
        'furniture/<str:slug>/activate/',
        apis.ActivateFurnitureApiView.as_view(),
        name='activate_furniture'
    ),
    path(
        'furniture/<str:slug>/deactivate/',
        apis.DeactivateFurnitureApiView.as_view(),
        name='deactivate_furniture'
    ),

    # ============= Company URL's ============= #
    path(
        'companies/active/',
        apis.ActiveCompaniesApiView.as_view(),
        name='active_company'
    ),
    path('companies/all/', apis.CompanyApiView.as_view(), name='company'),
    path(
        'company/<str:slug>/activate/',
        apis.ActivateCompanyApiView.as_view(),
        name='activate_company'
    ),
    path(
        'company/<str:slug>/deactivate/',
        apis.DeactivateCompanyApiView.as_view(),
        name='deactivate_company'
    ),
    path(
        'company/<str:slug>/delete/',
        apis.DeleteCompanyApiView.as_view(),
        name='delete_furniture'
    ),

    # ============= Category URL's ============= #
    path(
        'categories/all/',
        apis.CategoryApiView.as_view(),
        name='categories'
    ),
    path(
        'category/<str:slug>/activate/',
        apis.ActivateCategoryApiView.as_view(),
        name='activate_category'
    ),
    path(
        'category/<str:slug>/deactivate/',
        apis.DeactivateCategoryApiView.as_view(),
        name='deactivate_category'
    ),
]
