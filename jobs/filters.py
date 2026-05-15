import django_filters
from .models import Job


class JobFilter(django_filters.FilterSet):
    title    = django_filters.CharFilter(lookup_expr='icontains', label='Título contiene')
    company  = django_filters.CharFilter(lookup_expr='icontains', label='Empresa contiene')
    location = django_filters.CharFilter(lookup_expr='icontains', label='Ubicación contiene')
    remote   = django_filters.BooleanFilter(label='Solo remoto')
    source   = django_filters.ChoiceFilter(choices=Job.SOURCE_CHOICES, label='Fuente')
    from_date = django_filters.DateFilter(field_name='date_posted', lookup_expr='gte', label='Desde fecha')
    to_date   = django_filters.DateFilter(field_name='date_posted', lookup_expr='lte', label='Hasta fecha')

    class Meta:
        model  = Job
        fields = ['title', 'company', 'location', 'remote', 'source', 'from_date', 'to_date']
