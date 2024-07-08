from rest_framework import generics
from rest_framework import filters
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import Client, Telephone, Diagnostic, Panne, Outil, Reparation, Facture, CustomUser
from .serializers import ClientSerializer, TelephoneSerializer, DiagnosticSerializer, PanneSerializer, OutilSerializer, ReparationSerializer, FactureSerializer, CustomUserSerializer
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom','prenom']

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.order_by('-created_time')
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom','prenom', 'phone']

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.order_by('-created_time')
    serializer_class = ClientSerializer

class TelephoneListCreateView(generics.ListCreateAPIView):
    queryset = Telephone.objects.order_by('-created_time')
    serializer_class = TelephoneSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['imei', 'modele', 'marque']

class TelephoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Telephone.objects.order_by('-created_time')
    serializer_class = TelephoneSerializer

class DiagnosticListCreateView(generics.ListCreateAPIView):
    queryset = Diagnostic.objects.order_by('-created_time')
    serializer_class = DiagnosticSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['telephone__client__prenom', 'telephone__client__phone', 'telephone__imei']

class DiagnosticDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diagnostic.objects.order_by('-created_time')
    serializer_class = DiagnosticSerializer

class PanneListCreateView(generics.ListCreateAPIView):
    queryset = Panne.objects.order_by('-created_time')
    serializer_class = PanneSerializer

class PanneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Panne.objects.order_by('-created_time')
    serializer_class = PanneSerializer

class OutilListCreateView(generics.ListCreateAPIView):
    queryset = Outil.objects.order_by('-created_time')
    serializer_class = OutilSerializer

class OutilDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Outil.objects.order_by('-created_time')
    serializer_class = OutilSerializer

class ReparationListCreateView(generics.ListCreateAPIView):
    queryset = Reparation.objects.order_by('-created_time')
    serializer_class = ReparationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['numero_reparation']

class ReparationWithouFactureView(generics.ListAPIView):
    queryset = Reparation.objects.order_by('-created_time')
    serializer_class = ReparationSerializer

    def get_queryset(self):
        # Filtrer les réparations sans facture
        return Reparation.objects.filter(facture__isnull=True).order_by('-created_time')

class ReparationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reparation.objects.order_by('-created_time')
    serializer_class = ReparationSerializer

class FactureListCreateView(generics.ListCreateAPIView):
    queryset = Facture.objects.order_by('-created_time')
    serializer_class = FactureSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['numero_facture']

class FactureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facture.objects.order_by('-created_time')
    serializer_class = FactureSerializer
