from rest_framework import generics
from rest_framework import filters
from .models import Client, Telephone, Diagnostic, Panne, Outil, Reparation, Facture
from .serializers import ClientSerializer, TelephoneSerializer, DiagnosticSerializer, PanneSerializer, OutilSerializer, ReparationSerializer, FactureSerializer

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom', 'phone']

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class TelephoneListCreateView(generics.ListCreateAPIView):
    queryset = Telephone.objects.all()
    serializer_class = TelephoneSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['imei', 'modele', 'marque']

class TelephoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Telephone.objects.all()
    serializer_class = TelephoneSerializer

class DiagnosticListCreateView(generics.ListCreateAPIView):
    queryset = Diagnostic.objects.all()
    serializer_class = DiagnosticSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['telephone__client__prenom', 'telephone__client__phone', 'telephone__imei']

class DiagnosticDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diagnostic.objects.all()
    serializer_class = DiagnosticSerializer

class PanneListCreateView(generics.ListCreateAPIView):
    queryset = Panne.objects.all()
    serializer_class = PanneSerializer

class PanneDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Panne.objects.all()
    serializer_class = PanneSerializer

class OutilListCreateView(generics.ListCreateAPIView):
    queryset = Outil.objects.all()
    serializer_class = OutilSerializer

class OutilDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Outil.objects.all()
    serializer_class = OutilSerializer

class ReparationListCreateView(generics.ListCreateAPIView):
    queryset = Reparation.objects.all()
    serializer_class = ReparationSerializer

class ReparationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reparation.objects.all()
    serializer_class = ReparationSerializer

class FactureListCreateView(generics.ListCreateAPIView):
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer

class FactureDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer
