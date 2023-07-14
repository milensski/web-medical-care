from django_filters import FilterSet, CharFilter

from web.app_auth.models import PatientProfile


class PatientFilter(FilterSet):

    civil_number = CharFilter(field_name='civil_number', lookup_expr='icontains')
    class Meta:
        model = PatientProfile
        fields = ('first_name', 'middle_name', 'last_name', 'civil_number')
