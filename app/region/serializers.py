from rest_framework import serializers
from .models import Region, District, Massive, Neighborhood, Farm


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        read_only_fields = ('created_at',)


class MassiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Massive
        fields = '__all__'
        read_only_fields = ('created_at',)


class DistrictGetSerializer(serializers.ModelSerializer):
    massives = MassiveSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = ('id', 'user', 'region', 'name', 'plan', 'crop_area', 'created_at', 'massives')
        extra_kwargs = {'created_at': {'read_only': True}}

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'user', 'region', 'name', 'plan', 'crop_area', 'created_at')
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
