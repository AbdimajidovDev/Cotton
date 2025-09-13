from django.urls import path
from .views import TerritoryReportAPIView

urlpatterns = [
    path("reports/territories/", TerritoryReportAPIView.as_view(), name="territory-reports"),
]
