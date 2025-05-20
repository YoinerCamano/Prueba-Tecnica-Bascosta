from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from contactos.views import ContactoViewSet

router = routers.DefaultRouter()
router.register(r'contactos', ContactoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]