from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import (
    Squad, SquadDailyPicking, Worker, WorkerDailyPicking,
    Territory, Scalesman, CottonPicker, CarDailyPicking
)
from .serializers import (
    SquadSerializer, SquadDailySerializer, WorkerSerializer, WorkerDailySerializer,
    TerritorySerializer, ScalesmanSerializer, CottonPickerSerializer, CarDailySerializer, StartSquadDailySerializer, EndSquadDailySerializer
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


@extend_schema(tags=['SquadDaily'])
class SquadDailyAPI(APIView):
    serializer_class = SquadDailySerializer

    def get(self, request):
        queryset = SquadDailyPicking.objects.all()
        serializer = SquadDailySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SquadDailySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['SquadDaily'])
class SquadDailyDetailAPI(APIView):
    serializer_class = SquadDailySerializer

    def get(self, request, pk):
        obj = get_object_or_404(SquadDailyPicking, pk=pk)
        serializer = SquadDailySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = get_object_or_404(SquadDailyPicking, pk=pk)
        serializer = SquadDailySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = get_object_or_404(SquadDailyPicking, pk=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['SquadDaily'])
class SquadDailyStartAPI(APIView):
    serializer_class = StartSquadDailySerializer
    def post(self, request, pk):
        obj = get_object_or_404(SquadDailyPicking, pk=pk)
        if obj.start_time:
            return Response({"detail": "This daily picking already started"}, status=status.HTTP_400_BAD_REQUEST)

        obj.start_time = timezone.now()
        obj.status = SquadDailyPicking.Status.active
        obj.save()
        return Response(SquadDailySerializer(obj).data, status=status.HTTP_200_OK)


@extend_schema(tags=['SquadDaily'])
class SquadDailyEndAPI(APIView):
    serializer_class = EndSquadDailySerializer
    def post(self, request, pk):
        obj = get_object_or_404(SquadDailyPicking, pk=pk)

        if not obj.start_time:
            return Response({"detail": "Start time not set yet."}, status=status.HTTP_400_BAD_REQUEST)

        if obj.end_time:
            return Response({"detail": "End time already set."}, status=status.HTTP_400_BAD_REQUEST)

        obj.end_time = timezone.now()
        obj.status = SquadDailyPicking.Status.finished
        obj.save()

        return Response(SquadDailySerializer(obj).data, status=status.HTTP_200_OK)


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
