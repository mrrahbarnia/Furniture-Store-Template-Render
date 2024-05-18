"""
Store app API's.
"""
from typing import Any
from django.db.models import QuerySet
from django.urls import reverse
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status, permissions
from drf_spectacular.utils import extend_schema

from common.pagination import (
    LimitOffsetPagination,
    get_paginated_response_context
)
from core.services.store import (
    get_furniture_by_slug,
    rate_furniture,
    activate_company,
    deactivate_company,
    activate_furniture,
    deactivate_furniture,
    delete_company,
    activate_category,
    deactivate_category,
    create_company
)
from core.selectors.store import (
    list_active_furniture,
    list_active_companies,
    list_all_companies,
    list_all_furniture,
    list_active_categories,
    list_all_categories
)
from .serializers import CompanyBaseSerializer
from ...models import (
    Furniture,
    Company,
    Category
)


# ================= Furniture Api's ================= #
class ActiveFurnitureApiView(APIView):
    """Furniture api for listing them."""

    class Pagination(LimitOffsetPagination):
        """Paginating data to get 10 items per page."""
        default_limit = 10

    class ActiveFilterInputSerializer(serializers.Serializer):
        """Filtering furniture with query parameters."""
        name__icontains = serializers.CharField(
            max_length=250, required=False
        )
        price__range = serializers.CharField(
            max_length=250, required=False
        )

    class ActiveFurnitureOutputSerializer(serializers.Serializer):
        """Output serializer for furniture model."""
        name = serializers.CharField(max_length=150)
        price = serializers.DecimalField(max_digits=8, decimal_places=2)
        # TODO:Validating image field by size.
        image = serializers.ImageField()
        views = serializers.IntegerField()
        company = serializers.CharField(source='company.name')
        category = serializers.CharField(source='category.name')
        abs_url = serializers.SerializerMethodField()
        average_rating = serializers.FloatField()

        def get_abs_url(self, furniture):
            request = self.context.get('request')
            path = reverse('store_api:furniture_detail', args=[furniture.slug])
            return request.build_absolute_uri(path)

    @extend_schema(
            responses=ActiveFurnitureOutputSerializer,
            parameters=[ActiveFilterInputSerializer]
    )
    def get(
        self, request, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        price__range parameter => Enter exact two digits comma separated.
        examples => "19, 25" --- "19, " --- ", 25"
        """
        filtered_serializer = self.ActiveFilterInputSerializer(
            data=request.query_params
        )
        filtered_serializer.is_valid(raise_exception=True)
        try:
            furniture: QuerySet[Furniture] = list_active_furniture(
                filters=filtered_serializer.validated_data
            )
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.ActiveFurnitureOutputSerializer,
            queryset=furniture,
            request=request,
            view=self
        )


class FurnitureDetailApiView(APIView):
    """Furniture detail API view."""

    class FurnitureDetailOutputSerializer(serializers.Serializer):
        """Serializing data for furniture detail API."""
        name = serializers.CharField(max_length=150)
        price = serializers.DecimalField(max_digits=8, decimal_places=2)
        stock = serializers.IntegerField()
        description = serializers.CharField(max_length=1000)
        # TODO:Validating image field by size.
        image = serializers.ImageField()
        produced_date = serializers.DateField()
        company = serializers.CharField(source='company.name')
        category = serializers.CharField(source='category.name')

    @extend_schema(responses=FurnitureDetailOutputSerializer)
    def get(
        self, request, slug: str, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        Getting a furniture by it's specific slug.
        """
        try:
            furniture: Furniture = get_furniture_by_slug(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        response = self.FurnitureDetailOutputSerializer(furniture).data
        return Response(response, status=status.HTTP_200_OK)


class RatingFurnitureApiView(APIView):
    """Rating furniture with authenticated users."""
    permission_classes = [permissions.IsAuthenticated]

    class RateSerializer(serializers.Serializer):
        """Validating rating limitation in serializer layer."""
        rate = serializers.IntegerField(
            validators=[
                MinValueValidator(limit_value=0),
                MaxValueValidator(limit_value=10)
            ],
            required=True
        )

    @extend_schema(request=RateSerializer)
    def post(
            self, request, slug: str, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        serializer = self.RateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            rate_furniture(
                user=request.user,
                slug=slug,
                rate=serializer.validated_data.get('rate')
            )
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return Response(status=status.HTTP_200_OK)


class FurnitureApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    class Pagination(LimitOffsetPagination):
        default_limit = 10
    
    class FurnitureInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=150)
        price = serializers.DecimalField(max_digits=8, decimal_places=2)
        stock = serializers.IntegerField()



    class FurnitureOutputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=150)
        price = serializers.DecimalField(max_digits=8, decimal_places=2)
        image = serializers.ImageField()
        company = serializers.CharField(source='company.name')
        category = serializers.CharField(source='category.name')
        is_active = serializers.BooleanField()

    def get(
            self, request, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        Getting all furniture only by admin users.
        """
        try:
            all_furniture: QuerySet[Furniture] = list_all_furniture()
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.FurnitureOutputSerializer,
            queryset=all_furniture,
            request=request,
            view=self
        )
    
    @extend_schema(
            request=FurnitureInputSerializer,
            responses=FurnitureOutputSerializer
    )
    def post(
            self, request, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        Creating furniture only by admin clients.
        """


class ActivateFurnitureApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(
            self, request, slug: str, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        Get a specific furniture by it's slug
        and turn is_active field to True for it.
        """
        try:
            activate_furniture(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return Response(status=status.HTTP_200_OK)


class DeactivateFurnitureApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(
            self, request, slug: str, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        Get a specific furniture by it's slug
        and turn is_active field to False for it.
        """
        try:
            deactivate_furniture(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return Response(status=status.HTTP_200_OK)


# ================= Company Api's ================= #
class CompanyApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    class AllCompanySerializer(CompanyBaseSerializer):
        # is_active = serializers.BooleanField()
        activate_deactivate_url = serializers.SerializerMethodField()

        def get_activate_deactivate_url(self, company: Company):
            request = self.context.get('request')
            if not company.is_active:
                path = reverse(
                    'store_api:activate_company', args=[company.slug]
                )
            elif company.is_active:
                path = reverse(
                    'store_api:deactivate_company', args=[company.slug]
                )
            return request.build_absolute_uri(path)

    @extend_schema(responses=AllCompanySerializer)
    def get(
            self, request, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        Listing all companies with AdminUser
        permission for activating or deactivating them.
        """
        try:
            all_companies: QuerySet[Company] = list_all_companies()
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        response = self.AllCompanySerializer(
            all_companies, many=True, context={'request': request}
        ).data
        return Response(response, status=status.HTTP_200_OK)

    @extend_schema(
            request=CompanyBaseSerializer,
            responses=CompanyBaseSerializer
    )
    def post(
            self, request, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        Creating companies only by admin users.
        """
        serializer = CompanyBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            company: Company = create_company(
                name=serializer.validated_data.get('name'),
                ceo=serializer.validated_data.get('ceo'),
                staff=serializer.validated_data.get('staff')
            )
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        response = CompanyBaseSerializer(company).data
        return Response(response, status=status.HTTP_201_CREATED)


class ActiveCompaniesApiView(APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    @extend_schema(responses=CompanyBaseSerializer)
    def get(
        self, request, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """Listing all active companies."""
        try:
            active_companies: QuerySet[Company] = list_active_companies()
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=CompanyBaseSerializer,
            queryset=active_companies,
            request=request,
            view=self
        )


class ActivateCompanyApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(
            self, request, slug: str, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        Activating an existing company by it's slug.
        """
        try:
            activate_company(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return Response(status=status.HTTP_200_OK)


class DeactivateCompanyApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(
            self, request, slug: str, *args: Any, **kwargs: None
    ) -> Response | serializers.ValidationError:
        """
        Deactivating an existing company by it's slug.
        """
        try:
            deactivate_company(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return Response(status=status.HTTP_200_OK)


class DeleteCompanyApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(
            self, request, slug: str, *args, **kwargs
    ) -> Response | serializers.ValidationError:
        """
        Delete a specific company with
        it's slug only by admin users.
        """
        try:
            delete_company(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


# ================= Category Api's ================= #
class ActiveCategoriesApiView(APIView):

    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class ActiveCategoriesOutputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=150)

    def get(
            self, request, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        Listing active categories by every users.
        """
        try:
            active_categories: QuerySet[Category] = list_active_categories()
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.ActiveCategoriesOutputSerializer,
            queryset=active_categories,
            request=request,
            view=self
        )


class CategoryApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    class OutputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=150)
        is_active = serializers.BooleanField()
        activate_deactivate_url = serializers.SerializerMethodField()

        def get_activate_deactivate_url(self, category: Category):
            request = self.context.get('request')
            if category.is_active:
                path = reverse(
                    'store_api:deactivate_category', args=[category.slug]
                )
            elif not category.is_active:
                path = reverse(
                    'store_api:activate_category', args=[category.slug]
                )
            return request.build_absolute_uri(path)

    @extend_schema(responses=[OutputSerializer])
    def get(
            self, request, *args: Any, **kwargs: Any
    ) -> Response | serializers.ValidationError:
        """
        Listing all categories only by admin users.
        """
        try:
            categories: QuerySet[Category] = list_all_categories()
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        response = self.OutputSerializer(
            categories, many=True, context={'request': request}
        ).data
        return Response(response, status=status.HTTP_200_OK)


class ActivateCategoryApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(
            self, request, slug: str, *args: Any, **kwargs: Any
    ) -> None:
        """
        Activate categories by their slug only by admin users.
        """
        try:
            activate_category(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return Response(status=status.HTTP_200_OK)


class DeactivateCategoryApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(
            self, request, slug: str, *args: Any, **kwargs: Any
    ) -> None:
        """
        Deactivate categories by their slug only by admin users.
        """
        try:
            deactivate_category(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return Response(status=status.HTTP_200_OK)
