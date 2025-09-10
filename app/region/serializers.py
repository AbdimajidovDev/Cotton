from rest_framework import serializers
from .models import Region, District, Massive, Neighborhood, Farm


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        read_only_fields = ('created_at',)


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
        read_only_fields = ('created_at',)


class MassiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Massive
        fields = '__all__'
        read_only_fields = ('created_at',)


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = '__all__'
        read_only_fields = ('created_at',)


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'
