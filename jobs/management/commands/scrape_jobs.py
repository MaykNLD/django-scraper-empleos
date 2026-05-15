"""
Management command: python manage.py scrape_jobs

Ejecuta el scraper y guarda nuevas ofertas en la BD.
Uso:
    python manage.py scrape_jobs                # Todas las fuentes
    python manage.py scrape_jobs --source arbeitnow
    python manage.py scrape_jobs --source remotive
"""
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from jobs.scraper import fetch_all, fetch_arbeitnow, fetch_remotive
from jobs.models import Job, ScraperRun

logger = logging.getLogger('jobs')


class Command(BaseCommand):
    help = 'Scrape job offers from public APIs and save to database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            choices=['all', 'arbeitnow', 'remotive'],
            default='all',
            help='Source to scrape (default: all)',
        )

    def handle(self, *args, **options):
        source = options['source']
        self.stdout.write(self.style.HTTP_INFO(f'\n🔍 Iniciando scraper — fuente: {source}'))

        # Crear registro de ejecución
        run = ScraperRun.objects.create(source=source)

        try:
            # Obtener datos
            if source == 'arbeitnow':
                raw_jobs = fetch_arbeitnow()
            elif source == 'remotive':
                raw_jobs = fetch_remotive()
            else:
                raw_jobs = fetch_all()

            self.stdout.write(f'   📥 {len(raw_jobs)} ofertas obtenidas de APIs')

            # Guardar en BD (update_or_create para evitar duplicados)
            new_count = 0
            for job_data in raw_jobs:
                external_id = job_data.pop('external_id')
                _, created = Job.objects.update_or_create(
                    external_id=external_id,
                    defaults=job_data,
                )
                if created:
                    new_count += 1

            # Actualizar registro de ejecución
            run.status     = 'success'
            run.jobs_found = len(raw_jobs)
            run.jobs_new   = new_count
            run.finished_at = timezone.now()
            run.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'   ✅ Completado — {new_count} nuevas, '
                    f'{len(raw_jobs) - new_count} actualizadas, '
                    f'total BD: {Job.objects.count()}'
                )
            )

        except Exception as e:
            run.status    = 'error'
            run.error_msg = str(e)
            run.finished_at = timezone.now()
            run.save()
            logger.error(f"Error en scrape_jobs: {e}", exc_info=True)
            self.stderr.write(self.style.ERROR(f'❌ Error: {e}'))
            raise
