from django.urls import path
from .views import (
    ClientListCreateView, ClientDetailView,
    TelephoneListCreateView, TelephoneDetailView,
    DiagnosticListCreateView, DiagnosticDetailView,
    PanneListCreateView, PanneDetailView,
    OutilListCreateView, OutilDetailView,
    ReparationListCreateView, ReparationDetailView,
    FactureListCreateView, FactureDetailView
)

urlpatterns = [
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

    path('factures/', FactureListCreateView.as_view(), name='facture-list-create'),
    path('factures/<int:pk>/', FactureDetailView.as_view(), name='facture-detail'),
]
