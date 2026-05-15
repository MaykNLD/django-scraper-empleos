import logging
from collections import Counter
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Job, ScraperRun
from .serializers import JobSerializer, JobListSerializer, ScraperRunSerializer
from .filters import JobFilter

logger = logging.getLogger('jobs')

# Skills técnicos a detectar
SKILL_KEYWORDS = [
    'python', 'javascript', 'typescript', 'nodejs', 'node.js',
    'react', 'vue', 'django', 'fastapi', 'flask', 'docker',
    'kubernetes', 'postgresql', 'mongodb', 'redis', 'aws',
    'gcp', 'azure', 'git', 'java', 'golang', 'rust',
    'machine learning', 'llm', 'ai', 'rest api', 'graphql',
    'microservices', 'linux', 'pandas', 'sql', 'supabase', 'firebase',
]


def _count_skills(jobs_qs) -> dict:
    """Cuenta ocurrencias de skills en títulos, descripciones y tags."""
    skill_counts = Counter()
    for job in jobs_qs.values('title', 'description', 'tags'):
        text = (job['title'] + ' ' + job['description']).lower()
        for skill in SKILL_KEYWORDS:
            if skill in text:
                skill_counts[skill] += 1
        # También contar desde tags
        for tag in (job['tags'] or []):
            skill_counts[tag.lower()] += 1

    return dict(skill_counts.most_common(20))


# ── Dashboard view ─────────────────────────────────────────────────────────────

def dashboard(request):
    """
    Vista principal — Dashboard de ofertas de trabajo con estadísticas.
    ⚠️ FRONTEND: Los templates los construimos por separado.
    """
    try:
        total        = Job.objects.count()
        remote_count = Job.objects.filter(remote=True).count()
        remote_pct   = round(remote_count / total * 100, 1) if total else 0
        by_source    = dict(Job.objects.values('source').annotate(n=Count('id')).values_list('source', 'n'))
        top_companies = list(
            Job.objects.values('company')
            .annotate(n=Count('id'))
            .order_by('-n')[:10]
            .values_list('company', 'n')
        )
        skills = _count_skills(Job.objects.all())
        last_runs = ScraperRun.objects.order_by('-started_at')[:5]
        latest_jobs = Job.objects.order_by('-fetched_at')[:20]

        context = {
            'total': total,
            'remote_count': remote_count,
            'remote_pct': remote_pct,
            'by_source': by_source,
            'top_skills': list(skills.items())[:15],
            'top_companies': top_companies,
            'last_runs': last_runs,
            'latest_jobs': latest_jobs,
        }
        return render(request, 'dashboard.html', context)

    except Exception as e:
        logger.error(f"Error en dashboard: {e}", exc_info=True)
        return render(request, 'error.html', {'message': str(e)}, status=500)


def stats_api(request):
    """API JSON rápida de estadísticas — usada por Chart.js."""
    try:
        total        = Job.objects.count()
        remote_count = Job.objects.filter(remote=True).count()
        by_source    = dict(Job.objects.values('source').annotate(n=Count('id')).values_list('source', 'n'))
        skills       = _count_skills(Job.objects.all())

        return JsonResponse({
            'total_jobs':    total,
            'remote_count':  remote_count,
            'remote_pct':    round(remote_count / total * 100, 1) if total else 0,
            'by_source':     by_source,
            'top_skills':    skills,
        })
    except Exception as e:
        logger.error(f"Error en stats_api: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


# ── DRF ViewSets ──────────────────────────────────────────────────────────────

class JobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API REST de ofertas de trabajo.

    GET /api/jobs/          — Lista paginada (20 por página)
    GET /api/jobs/{id}/     — Detalle de oferta
    GET /api/jobs/stats/    — Estadísticas agregadas
    GET /api/jobs/?remote=true&source=arbeitnow&title=python — Filtros
    """
    queryset         = Job.objects.all().order_by('-date_posted', '-fetched_at')
    filter_backends  = [DjangoFilterBackend]
    filterset_class  = JobFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        return JobSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """GET /api/jobs/stats/ — Estadísticas del mercado."""
        total        = self.get_queryset().count()
        remote_count = self.get_queryset().filter(remote=True).count()
        skills       = _count_skills(self.get_queryset())
        by_source    = dict(
            self.get_queryset().values('source')
            .annotate(n=Count('id'))
            .values_list('source', 'n')
        )
        return Response({
            'total_jobs':   total,
            'remote_pct':   round(remote_count / total * 100, 1) if total else 0,
            'by_source':    by_source,
            'top_skills':   skills,
        })


class ScraperRunViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/runs/  — Historial de ejecuciones del scraper.
    """
    queryset         = ScraperRun.objects.all().order_by('-started_at')
    serializer_class = ScraperRunSerializer
