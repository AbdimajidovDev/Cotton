from django.urls import path

from .views import (
    RegionAPI, RegionDetailAPI,
    DistrictAPI, DistrictDetailAPI,
    MassiveAPI, MassiveDetailAPI,
    NeighborhoodAPI, NeighborhoodDetailAPI,
    FarmAPI, FarmDetailAPI, FarmByMassiveAPI
)

app_name = 'region'

urlpatterns = [
    path("regions/", RegionAPI.as_view(), name="region-list-create"),
    path("regions/<int:pk>/", RegionDetailAPI.as_view(), name="region-detail"),

    path("districts/", DistrictAPI.as_view(), name="district-list-create"),
    path("districts/<int:pk>/", DistrictDetailAPI.as_view(), name="district-detail"),

    path("massives/", MassiveAPI.as_view(), name="massive-list-create"),
    path("massives/<int:pk>/", MassiveDetailAPI.as_view(), name="massive-detail"),
    path("massives/<int:pk>/farms/", FarmByMassiveAPI.as_view(), name="massive-detail"),

    path("neighborhoods/", NeighborhoodAPI.as_view(), name="neighborhood-list-create"),
    path("neighborhoods/<int:pk>/", NeighborhoodDetailAPI.as_view(), name="neighborhood-detail"),

    path("farms/", FarmAPI.as_view(), name="farm-list-create"),
    path("farms/<int:pk>/", FarmDetailAPI.as_view(), name="farm-detail"),
]

