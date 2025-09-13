from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from .models import (
    Squad, SquadDailyPicking, Worker, WorkerDailyPicking,
    Territory, Scalesman, CottonPicker, CarDailyPicking, Shtab
)
from .serializers import (
    SquadSerializer, SquadDailySerializer, WorkerSerializer, WorkerDailySerializer,
    TerritorySerializer, ScalesmanSerializer, CottonPickerSerializer, CarDailySerializer, StartSquadDailySerializer,
    EndSquadDailySerializer, SquadForShtabSerializer, ShtabSquadDailyCreateSerializer
)


@extend_schema(tags=['Squad'])
class SquadAPI(APIView):
    serializer_class = SquadSerializer

    def get(self, request):
        queryset = Squad.objects.all()
        serializer = SquadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SquadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Squad'])
class SquadDetailAPI(APIView):
    serializer_class = SquadSerializer

    def get(self, request, pk):
        squad = get_object_or_404(Squad, pk=pk)
        serializer = SquadSerializer(squad)
        return Response(serializer.data)

    def put(self, request, pk):
        squad = get_object_or_404(Squad, pk=pk)
        serializer = SquadSerializer(squad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        squad = get_object_or_404(Squad, pk=pk)
        squad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["SquadDaily"],
    request=StartSquadDailySerializer,
    responses={201: SquadDailySerializer}
)
class SquadDailyAPI(APIView):
    serializer_class = SquadDailySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        squads = Squad.objects.filter(user=request.user)
        if not squads.exists():
            return Response([], status=status.HTTP_200_OK)

        queryset = (
            SquadDailyPicking.objects
            .filter(squad__in=squads)
            .order_by('-created_at', '-start_time')
        )
        serializer = SquadDailySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        squads = Squad.objects.filter(user=request.user)
        squad_instance = squads.first()
        if not squad_instance:
            return Response({"detail": "User does not belong to any squad"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StartSquadDailySerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save(squad=squad_instance, start_time=timezone.now())
            return Response(SquadDailySerializer(obj).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['SquadDaily'])
class SquadDailyDetailAPI(APIView):
    serializer_class = SquadDailySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        squads = Squad.objects.filter(user=request.user)
        return get_object_or_404(SquadDailyPicking, pk=pk, squad__in=squads)

    def get(self, request, pk):
        obj = self.get_object(request, pk)
        serializer = SquadDailySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(request, pk)
        serializer = SquadDailySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(request, pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['SquadDaily'])
class SquadDailyStartAPI(APIView):
    serializer_class = StartSquadDailySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        squads = Squad.objects.filter(user=request.user)
        squad_instance = squads.first()
        if not squad_instance:
            return Response({"detail": "User does not belong to any squad"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = StartSquadDailySerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save(squad=squad_instance, start_time=timezone.now())
            return Response(SquadDailySerializer(obj).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['SquadDaily'])
class SquadDailyEndAPI(APIView):
    serializer_class = EndSquadDailySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        squads = Squad.objects.filter(user=request.user)
        return get_object_or_404(SquadDailyPicking, pk=pk, squad__in=squads)

    def post(self, request, pk):
        obj = self.get_object(request, pk)

        if not obj.start_time:
            return Response({"detail": "Start time not set yet."}, status=status.HTTP_400_BAD_REQUEST)

        if obj.end_time:
            return Response({"detail": "End time already set."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EndSquadDailySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(end_time=timezone.now(), status=SquadDailyPicking.Status.finished)
            return Response(SquadDailySerializer(obj).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['SquadDaily'])
class SquadDailyTodayAPI(APIView):
    serializer_class = SquadDailySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = now().date()
        squads = Squad.objects.filter(user=request.user)

        queryset = SquadDailyPicking.objects.filter(
            squad__in=squads,
            created_at__date=today
        ).order_by('-created_at')

        serializer = SquadDailySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=['Worker'])
class WorkerAPI(APIView):
    serializer_class = WorkerSerializer

    def get(self, request):
        queryset = Worker.objects.all()
        serializer = WorkerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Worker'])
class WorkerDetailAPI(APIView):
    serializer_class = WorkerSerializer

    def get(self, request, pk):
        obj = get_object_or_404(Worker, pk=pk)
        serializer = WorkerSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = get_object_or_404(Worker, pk=pk)
        serializer = WorkerSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Worker, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['WorkerDaily'])
class WorkerDailyAPI(APIView):
    serializer_class = WorkerDailySerializer

    def get(self, request):
        queryset = WorkerDailyPicking.objects.all()
        serializer = WorkerDailySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkerDailySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['WorkerDaily'])
class WorkerDailyDetailAPI(APIView):
    serializer_class = WorkerDailySerializer

    def get(self, request, pk):
        obj = get_object_or_404(WorkerDailyPicking, pk=pk)
        serializer = WorkerDailySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = get_object_or_404(WorkerDailyPicking, pk=pk)
        serializer = WorkerDailySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(WorkerDailyPicking, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Territory'])
class TerritoryAPI(APIView):
    serializer_class = TerritorySerializer

    def get(self, request):
        queryset = Territory.objects.all()
        serializer = TerritorySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TerritorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Territory'])
class TerritoryDetailAPI(APIView):
    serializer_class = TerritorySerializer

    def get(self, request, pk):
        obj = get_object_or_404(Territory, pk=pk)
        serializer = TerritorySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = get_object_or_404(Territory, pk=pk)
        serializer = TerritorySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Territory, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Scalesman'])
class ScalesmanAPI(APIView):
    serializer_class = ScalesmanSerializer

    def get(self, request):
        queryset = Scalesman.objects.all()
        serializer = ScalesmanSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ScalesmanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Scalesman'])
class ScalesmanDetailAPI(APIView):
    serializer_class = ScalesmanSerializer

    def get(self, request, pk):
        obj = get_object_or_404(Scalesman, pk=pk)
        serializer = ScalesmanSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = get_object_or_404(Scalesman, pk=pk)
        serializer = ScalesmanSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(Scalesman, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['CottonPicker'])
class CottonPickerAPI(APIView):
    serializer_class = CottonPickerSerializer

    def get(self, request):
        queryset = CottonPicker.objects.all()
        serializer = CottonPickerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CottonPickerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['CottonPicker'])
class CottonPickerDetailAPI(APIView):
    serializer_class = CottonPickerSerializer

    def get(self, request, pk):
        obj = get_object_or_404(CottonPicker, pk=pk)
        serializer = CottonPickerSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = get_object_or_404(CottonPicker, pk=pk)
        serializer = CottonPickerSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(CottonPicker, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['CarDaily'])
class CarDailyAPI(APIView):
    serializer_class = CarDailySerializer

    def get(self, request):
        queryset = CarDailyPicking.objects.all()
        serializer = CarDailySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CarDailySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['CarDaily'])
class CarDailyDetailAPI(APIView):
    serializer_class = CarDailySerializer

    def get(self, request, pk):
        obj = get_object_or_404(CarDailyPicking, pk=pk)
        serializer = CarDailySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = get_object_or_404(CarDailyPicking, pk=pk)
        serializer = CarDailySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(CarDailyPicking, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Shtab"])
class ShtabAPI(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShtabSquadDailyCreateSerializer

    def get(self, request):
        squads = Squad.objects.all()
        serializer = SquadForShtabSerializer(squads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=ShtabSquadDailyCreateSerializer, responses=ShtabSquadDailyCreateSerializer)
    def post(self, request):
        serializer = ShtabSquadDailyCreateSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(ShtabSquadDailyCreateSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
