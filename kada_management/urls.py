from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    ClientListCreateView, ClientDetailView, ClientStatisticView, RentabiliteView,
    TelephoneListCreateView, TelephoneDetailView,
    DiagnosticListCreateView, DiagnosticDetailView,
    ReparationListCreateView, ReparationDetailView,
    FactureListCreateView, FactureDetailView,
    ReparationWithouFactureView, UserCount, UserListCreateView,
    UserDetailView, CustomTokenObtainPairView
)

urlpatterns = [
    path("auth/", obtain_auth_token),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users_count/', UserCount.as_view(), name='users-count'),

    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clientstate/', ClientStatisticView.as_view(), name='clientstate'),


    path('telephones/', TelephoneListCreateView.as_view(), name='telephone-list-create'),
    path('telephones/<int:pk>/', TelephoneDetailView.as_view(), name='telephone-detail'),

    path('diagnostics/', DiagnosticListCreateView.as_view(), name='diagnostic-list-create'),
    path('diagnostics/<int:pk>/', DiagnosticDetailView.as_view(), name='diagnostic-detail'),

    path('reparations/', ReparationListCreateView.as_view(), name='reparation-list-create'),
    path('reparations/<int:pk>/', ReparationDetailView.as_view(), name='reparation-detail'),
    path('reparations_facture/', ReparationWithouFactureView.as_view(), name='repation_facture'),

    path('factures/', FactureListCreateView.as_view(), name='facture-list-create'),
    path('factures/<int:pk>/', FactureDetailView.as_view(), name='facture-detail'),
    path('rentabilite/', RentabiliteView.as_view(), name='rentabilite'),
]
