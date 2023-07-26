from django_filters import FilterSet, CharFilter, ChoiceFilter

from web.app_auth.models import PatientProfile, Appointment


class PatientFilter(FilterSet):
    civil_number = CharFilter(field_name='civil_number', label='PIN', lookup_expr='contains')

    class Meta:
        model = PatientProfile
        fields = ('first_name', 'last_name', 'civil_number')


class AppointmentFilter(FilterSet):
    # query = PatientProfile.objects.filter(appointment__status__in=['Rejected', 'Canceled', 'Approved']).
    # appointments = [(x, x) for x in query]

    status = ChoiceFilter(choices=Appointment.STATUS)

    # patient = ChoiceFilter(choices=appointments)

    class Meta:
        model = Appointment
        fields = ('patient', 'status')
