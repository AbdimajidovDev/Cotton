from django.urls import path, include


urlpatterns = [

    path('users/', include('app.users.urls')),
    path('region/', include('app.region.urls')),
    path('squad/', include('app.squad.urls')),
]