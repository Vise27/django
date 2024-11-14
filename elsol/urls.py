from django.urls import path, include
from rest_framework import routers
from . import views  
from .views import CategoriaViewSet,FavoritoViewSet, EmpleadoViewSet, VentaViewSet, ProveedorViewSet, ProductoViewSet, DetalleVentaViewSet, InventarioViewSet

router = routers.DefaultRouter()

router.register(r'categorias', CategoriaViewSet)
router.register(r'empleados', EmpleadoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'detalles_venta', DetalleVentaViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'favorito',FavoritoViewSet)

urlpatterns = [
    path('', include(router.urls)),  #
]