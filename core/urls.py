from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('Auth.urls')),
    path('api/', include('pqrsAPI.urls')),
    path('api/contratacion/', include('contratacionAPI.urls')),
    path('api/inspección/', include('InspecciónAPI.urls')),
    path('api/sisben/', include('sisbenAPI.urls')),
    path('api/ticket/', include('ticketAPI.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

