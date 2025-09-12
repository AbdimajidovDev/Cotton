from drf_spectacular.utils import extend_schema
from .serializers import RegionSerializer, DistrictSerializer, MassiveSerializer, NeighborhoodSerializer, \
    FarmSerializer, DistrictGetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Region, District, Massive, Neighborhood, Farm


@extend_schema(tags=['Region'])
class RegionAPI(APIView):
    serializer_class = RegionSerializer
    def get(self, request):
        regions = Region.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Region'])
class RegionDetailAPI(APIView):
    serializer_class = RegionSerializer
    def get(self, request, pk):
        region = get_object_or_404(Region, pk=pk)
        serializer = RegionSerializer(region)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        region = get_object_or_404(Region, pk=pk)
        serializer = RegionSerializer(region, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        region = get_object_or_404(Region, pk=pk)
        region.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Farm'])
class FarmAPI(APIView):
    serializer_class = FarmSerializer
    def get(self, request):
        farms = Farm.objects.all()
        serializer = FarmSerializer(farms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FarmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Farm'])
class FarmDetailAPI(APIView):
    serializer_class = FarmSerializer
    def get(self, request, pk):
        farm = get_object_or_404(Farm, pk=pk)
        serializer = FarmSerializer(farm)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        farm = get_object_or_404(Farm, pk=pk)
        serializer = FarmSerializer(farm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        farm = get_object_or_404(Farm, pk=pk)
        farm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['District'])
class DistrictAPI(APIView):
    serializer_class = DistrictGetSerializer

    def get(self, request):
        districts = District.objects.all()
        serializer = DistrictGetSerializer(districts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DistrictSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['District'])
class DistrictDetailAPI(APIView):
    serializer_class = DistrictSerializer
    def get(self, request, pk):
        district = get_object_or_404(District, pk=pk)
        serializer = DistrictSerializer(district)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        district = get_object_or_404(District, pk=pk)
        serializer = DistrictSerializer(district, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        district = get_object_or_404(District, pk=pk)
        district.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Massive'])
class MassiveAPI(APIView):
    serializer_class = MassiveSerializer
    def get(self, request):
        massive = Massive.objects.all()
        serializer = MassiveSerializer(massive, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MassiveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Massive'])
class MassiveDetailAPI(APIView):
    serializer_class = MassiveSerializer
    def get(self, request, pk):
        massive = get_object_or_404(Massive, pk=pk)
        serializer = MassiveSerializer(massive)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        massive = get_object_or_404(Massive, pk=pk)
        serializer = MassiveSerializer(massive, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        massive = get_object_or_404(Massive, pk=pk)
        massive.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Neighborhood'])
class NeighborhoodAPI(APIView):
    serializer_class = NeighborhoodSerializer
    def get(self, request):
        neighborhoods = Neighborhood.objects.all()
        serializer = NeighborhoodSerializer(neighborhoods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NeighborhoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Neighborhood'])
class NeighborhoodDetailAPI(APIView):
    serializer_class = NeighborhoodSerializer
    def get(self, request, pk):
        neighborhood = get_object_or_404(Neighborhood, pk=pk)
        serializer = NeighborhoodSerializer(neighborhood)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        neighborhood = get_object_or_404(Neighborhood, pk=pk)
        serializer = NeighborhoodSerializer(neighborhood, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        neighborhood = get_object_or_404(Neighborhood, pk=pk)
        neighborhood.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
