from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from app.squad.models import Territory
from .serializers import RegionReportSerializer
from ..region.models import Region


class RegionReportAPIView(APIView):
    serializer_class = RegionReportSerializer

    def get(self, request, pk):
        region = get_object_or_404(Region, pk=pk)
        serializer = RegionReportSerializer(region)
        return Response(serializer.data, status=status.HTTP_200_OK)
