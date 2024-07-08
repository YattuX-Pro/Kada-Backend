from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    ClientListCreateView, ClientDetailView,
    TelephoneListCreateView, TelephoneDetailView,
    DiagnosticListCreateView, DiagnosticDetailView,
    PanneListCreateView, PanneDetailView,
    OutilListCreateView, OutilDetailView,
    ReparationListCreateView, ReparationDetailView,
    FactureListCreateView, FactureDetailView,
    ReparationWithouFactureView, UserListCreateView,
    UserDetailView, CustomTokenObtainPairView
)

urlpatterns = [
    path("auth/", obtain_auth_token),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),

    path('telephones/', TelephoneListCreateView.as_view(), name='telephone-list-create'),
    path('telephones/<int:pk>/', TelephoneDetailView.as_view(), name='telephone-detail'),

    path('diagnostics/', DiagnosticListCreateView.as_view(), name='diagnostic-list-create'),
    path('diagnostics/<int:pk>/', DiagnosticDetailView.as_view(), name='diagnostic-detail'),

    path('pannes/', PanneListCreateView.as_view(), name='panne-list-create'),
    path('pannes/<int:pk>/', PanneDetailView.as_view(), name='panne-detail'),

    path('outils/', OutilListCreateView.as_view(), name='outil-list-create'),
    path('outils/<int:pk>/', OutilDetailView.as_view(), name='outil-detail'),

    path('reparations/', ReparationListCreateView.as_view(), name='reparation-list-create'),
    path('reparations/<int:pk>/', ReparationDetailView.as_view(), name='reparation-detail'),
    path('reparations_facture/', ReparationWithouFactureView.as_view(), name='repation_facture'),

    path('factures/', FactureListCreateView.as_view(), name='facture-list-create'),
    path('factures/<int:pk>/', FactureDetailView.as_view(), name='facture-detail'),
]
