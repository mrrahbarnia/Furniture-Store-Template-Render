"""
Filter existing furniture with provided query parameters.
"""
from decimal import Decimal
from django.db.models import QuerySet
from rest_framework.exceptions import APIException
from django_filters import (
    FilterSet,
    CharFilter
)

from store.models import Furniture


class FurnitureFilter(FilterSet):
    """Custom filter on listing furniture endpoint."""

    name__icontains: str = CharFilter(method='filter_name__icontains')
    price__range: str = CharFilter(method='filter_price__range')

    def filter_name__icontains(
            self, queryset: QuerySet[Furniture], name: str | None, value: str
    ) -> QuerySet[Furniture]:
        return queryset.filter(name__icontains=value)

    def filter_price__range(
            self, queryset: QuerySet[Furniture], name: str | None, value: str
    ) -> QuerySet[Furniture] | APIException:
        """
        Two price comma separated.
        """
        limit: int = 2
        price__range: list[str] = value.split(',')  # '19, 125'
        if len(price__range) > limit:
            raise APIException(
                f'The price__range parameter must be \
                    equal to {limit} price with comma separated.'
            )
        price__range_0, price__range_1 = price__range

        if not price__range_0:
            return queryset.filter(price__lte=Decimal(price__range_1))
        if not price__range_1:
            return queryset.filter(price__gte=Decimal(price__range_0))

        return queryset.filter(
            price__range=(Decimal(price__range_0), Decimal(price__range_1))
        )

    class Meta:
        model = Furniture
        fields = [
            'slug'
        ]
