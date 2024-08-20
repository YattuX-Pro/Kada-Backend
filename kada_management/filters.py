from django_filters import rest_framework as filters
from rest_framework.pagination import LimitOffsetPagination

from kada_management.models import CustomUser

class UserFilters(filters.FilterSet):
    is_commercial = filters.BooleanFilter()
    is_active = filters.BooleanFilter()
    is_technician = filters.BooleanFilter()
    is_superuser = filters.BooleanFilter()

    class Meta:
        model = CustomUser
        fields = ['is_commercial','is_active','is_technician','is_superuser']

class CustomLimitOffsetPagination(LimitOffsetPagination):
    def get_limit(self, request):
        limit = super().get_limit(request)
        if limit == 0:
            return None  
        return limit