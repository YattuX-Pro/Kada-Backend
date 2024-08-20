from rest_framework import generics
from rest_framework import filters
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import timedelta
from django.db.models import Count


from kada_management.filters import UserFilters


from .models import Client, Telephone, Diagnostic, Reparation, Facture, CustomUser
from .serializers import ClientSerializer, TelephoneSerializer, DiagnosticSerializer, ReparationSerializer, FactureSerializer, CustomUserSerializer
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filterset_class = UserFilters
    filter_backends = [filters.SearchFilter,DjangoFilterBackend]
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
    search_fields = ['telephone__client__prenom', 'telephone__client__phone', 'telephone__imei','diagnostic_type']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if(self.request.user.is_technician):
            return Diagnostic.objects.filter(user=self.request.user).order_by('-created_time')
        return Diagnostic.objects.filter().order_by('-created_time')


class DiagnosticDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diagnostic.objects.order_by('-created_time')
    serializer_class = DiagnosticSerializer


class ReparationListCreateView(generics.ListCreateAPIView):
    queryset = Reparation.objects.order_by('-created_time')
    serializer_class = ReparationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['numero_reparation','status']

    def get_queryset(self):
        if(self.request.user.is_commercial):
            return Reparation.objects.filter(commercial=self.request.user).order_by('-created_time')

        if(self.request.user.is_technician):
            return Reparation.objects.filter(technician=self.request.user).order_by('-created_time')
        return Reparation.objects.filter().order_by('-created_time')


class ReparationWithouFactureView(generics.ListAPIView):
    queryset = Reparation.objects.order_by('-created_time')
    serializer_class = ReparationSerializer

    def get_queryset(self):
        if(self.request.user.is_commercial):
            return Reparation.objects.filter(facture__isnull=True, status="completed", commercial=self.request.user).order_by('-created_time')

        if(self.request.user.is_technician):
            return Reparation.objects.filter(facture__isnull=True, status="completed",technician=self.request.user).order_by('-created_time')
        return Reparation.objects.filter().order_by('-created_time')
    

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


class RentabiliteView(APIView):
    def get(self, request):
        un_an_avant = timezone.now() - timedelta(days=365)
        
        factures_par_mois = Facture.objects.filter(
            created_time__gte = un_an_avant
        ).annotate(
            mois=TruncMonth('created_time')
        ).values('mois').annotate(
            total=Sum('montant_total')
        ).order_by('mois')

        labels = []
        data = []


        for facture in factures_par_mois:
            labels.append(facture['mois'].strftime('%B %Y'))
            data.append(float(facture['total']))

        chart_data = {
            'labels': labels,
            'datasets': [
                {
                    'data': data,
                    'label': 'Montant facturé'
                }
            ]
        }
        return Response(chart_data)
    
class ClientStatisticView(APIView):
    def get(self, request):
        un_an_avant = timezone.now() - timedelta(days=365)
        
        clients_par_mois = Client.objects.filter(
            created_time__gte = un_an_avant
        ).annotate(
            mois=TruncMonth('created_time')
        ).values('mois').annotate(
            total=Count('id')
        ).order_by('mois')

        labels = []
        data = []

        for client in clients_par_mois:
            labels.append(client['mois'].strftime('%B %Y'))
            data.append(float(client['total']))

        chart_data = {
            'labels': labels,
            'datasets': [
                {
                    'data': data,
                    'label': 'Montant facturé'
                }
            ]
        }
        return Response(chart_data)
    
class UserCount(APIView):
    
    def get(self, request):

        admins = CustomUser.objects.filter(is_superuser = True).count()
        technicians = CustomUser.objects.filter(is_technician = True).count()
        sellers = CustomUser.objects.filter(is_commercial = True).count()
        clients = Client.objects.all().count()

        data = {
            'admins': admins,
            'technicians': technicians,
            'sellers': sellers,
            'clients': clients,
        }

        return Response(data)