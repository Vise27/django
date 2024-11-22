from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from django.shortcuts import render
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    Categoria, Venta, Proveedor, Producto, DetalleVenta, 
    Favorito, User, Carrito, Factura, CarritoItem
)
from .serializer import (
    UserSerializer, CategoriaSerializer, VentaSerializer, ProveedorSerializer, 
    ProductoSerializer, DetalleVentaSerializer, FavoritoSerializer, 
    RegisterSerializer, CarritoSerializer, FacturaSerializer, CarritoItemSerializer
)

def producto_mas_vendido_view(request):
    producto_mas_vendido = DetalleVenta.objects.values('producto__nombre').annotate(
        total_vendido=Sum('cantidad')
    ).order_by('-total_vendido').first()

    return render(request, 'admin/producto_mas_vendido.html', {
        'producto_mas_vendido': producto_mas_vendido
    })

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = (DjangoFilterBackend,)  
    filterset_fields = ['codigo']

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer


class FavoritoViewSet(viewsets.ModelViewSet):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(User=self.request.user)


class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtrar carritos por usuario autenticado
        return Carrito.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Evitar la creación de un carrito duplicado para el mismo usuario
        if not Carrito.objects.filter(usuario=self.request.user).exists():
            serializer.save(usuario=self.request.user)


class CarritoItemViewSet(viewsets.ModelViewSet):
    queryset = CarritoItem.objects.all()
    serializer_class = CarritoItemSerializer


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            user = User.objects.get(username=request.data['username'])
            data['user_id'] = user.id
            data['username'] = user.username
            return Response(data, status=status.HTTP_200_OK)
        return Response(response.data, status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Crear el usuario
            user = serializer.save()
            
            # Verificar si ya existe un carrito para el usuario
            if not Carrito.objects.filter(usuario=user).exists():
                # Crear el carrito asociado al usuario solo si no existe
                Carrito.objects.create(usuario=user)
            
            # Serializar los datos del usuario
            user_data = UserSerializer(user).data
            
            return Response({
                "message": "Usuario registrado exitosamente!",
                "user": user_data
            }, status=status.HTTP_201_CREATED)
        
        # Si el serializer no es válido, se devuelven los errores
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
