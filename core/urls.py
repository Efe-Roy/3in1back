
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Auth.urls')),
    path('api/', include('pqrsAPI.urls')),
    path('api/contratacion/', include('contratacionAPI.urls')),
    path('api/inspección/', include('InspecciónAPI.urls')),
]
