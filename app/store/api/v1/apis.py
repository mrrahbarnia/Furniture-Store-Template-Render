"""
Store app API's.
"""
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from drf_spectacular.utils import extend_schema

# from django.urls import reverse
from common.pagination import (
    LimitOffsetPagination,
    get_paginated_response_context
)
from core.services.store import (
    get_furniture_by_slug
)
from core.selectors.store import (
    list_active_furniture
)


class FurnitureApiView(APIView):
    """Furniture api for listing them."""

    class Pagination(LimitOffsetPagination):
        """Paginating data to get 10 items per page."""
        default_limit = 10

    class FurnitureOutputSerializer(serializers.Serializer):
        """Output serializer for furniture model."""
        name = serializers.CharField(max_length=150)
        price = serializers.DecimalField(max_digits=8, decimal_places=2)
        # TODO:Validating image field by size.
        image = serializers.ImageField()
        views = serializers.IntegerField()
        company = serializers.CharField(source='company.name')
        category = serializers.CharField(source='category.name')
        abs_url = serializers.SerializerMethodField()

        def get_abs_url(self, furniture):
            request = self.context.get('request')
            path = reverse('store_api:furniture_detail', args=[furniture.slug])
            return request.build_absolute_uri(path)

    @extend_schema(responses=FurnitureOutputSerializer)
    def get(self, request) -> Response | serializers.ValidationError:
        try:
            furniture = list_active_furniture()
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.FurnitureOutputSerializer,
            queryset=furniture,
            request=request,
            view=self
        )


class FurnitureDetailApiView(APIView):

    class FurnitureDetailOutputSerializer(serializers.Serializer):
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
        self, request, slug: str
    ) -> Response | serializers.ValidationError:
        """
        Getting a furniture by it's specific slug.
        """
        try:
            furniture = get_furniture_by_slug(slug=slug)
        except Exception as ex:
            raise serializers.ValidationError(
                {'error': f'{ex}'}
            )
        response = self.FurnitureDetailOutputSerializer(furniture).data
        return Response(response, status=status.HTTP_200_OK)
