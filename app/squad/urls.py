from django.urls import path


from .views import (
    SquadAPI, SquadDetailAPI,
    SquadDailyAPI, SquadDailyDetailAPI,
    WorkerAPI, WorkerDailyAPI, WorkerDailyDetailAPI,
    TerritoryAPI, TerritoryDetailAPI,
    ScalesmanAPI, ScalesmanDetailAPI,
    CottonPickerAPI, CottonPickerDetailAPI,
    CarDailyAPI, CarDailyDetailAPI, WorkerDetailAPI
)

app_name = 'squad'

urlpatterns = [
    path("squads/", SquadAPI.as_view(), name="squad-list"),
    path("squads/<int:pk>/", SquadDetailAPI.as_view(), name="squad-detail"),

    path("squad-daily/", SquadDailyAPI.as_view(), name="squad-daily-list"),
    path("squad-daily/<int:pk>/", SquadDailyDetailAPI.as_view(), name="squad-daily-detail"),

    path("workers/", WorkerAPI.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailAPI.as_view(), name="worker-detail"),

    path("worker-daily/", WorkerDailyAPI.as_view(), name="worker-daily-list"),
    path("worker-daily/<int:pk>/", WorkerDailyDetailAPI.as_view(), name="worker-daily-detail"),

    path("territories/", TerritoryAPI.as_view(), name="territory-list"),
    path("territories/<int:pk>/", TerritoryDetailAPI.as_view(), name="territory-detail"),

    path("scalesmen/", ScalesmanAPI.as_view(), name="scalesman-list"),
    path("scalesmen/<int:pk>/", ScalesmanDetailAPI.as_view(), name="scalesman-detail"),

    path("cotton-pickers/", CottonPickerAPI.as_view(), name="cotton-picker-list"),
    path("cotton-pickers/<int:pk>/", CottonPickerDetailAPI.as_view(), name="cotton-picker-detail"),

    path("car-daily/", CarDailyAPI.as_view(), name="car-daily-list"),
    path("car-daily/<int:pk>/", CarDailyDetailAPI.as_view(), name="car-daily-detail"),
]

