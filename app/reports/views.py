from rest_framework.views import APIView
from rest_framework.response import Response
from app.squad.models import Territory
from .serializers import TerritoryReportSerializer

class TerritoryReportAPIView(APIView):
    def get(self, request):
        territories = Territory.objects.all()
        serializer = TerritoryReportSerializer(territories, many=True)
        return Response(serializer.data)
