from django.urls import path
from .views import RegionReportAPIView

urlpatterns = [
    path("reports/regions/<int:pk>/", RegionReportAPIView.as_view(), name="territory-reports"),
]
