"""
Base serializers.
"""
from rest_framework import serializers


class CompanyBaseSerializer(serializers.Serializer):
    """
    Base serializer for companies to
    inheriting from it by other serializers
    """
    slug = serializers.CharField(max_length=250)
    name = serializers.CharField(max_length=150)
    ceo = serializers.CharField(max_length=100)
    staff = serializers.IntegerField()
