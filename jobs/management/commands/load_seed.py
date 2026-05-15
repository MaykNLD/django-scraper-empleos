"""
Management command: python manage.py load_seed

Carga 200 ofertas de demo desde seed_data.json.
Útil para ver el dashboard sin necesitar APIs externas.
"""
import json
import logging
from pathlib import Path
from django.core.management.base import BaseCommand
from jobs.models import Job

logger = logging.getLogger('jobs')
SEED_FILE = Path(__file__).resolve().parent.parent.parent.parent / 'fixtures' / 'seed_jobs.json'


class Command(BaseCommand):
    help = 'Load 200 seed job offers for demo purposes'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing jobs first')

    def handle(self, *args, **options):
        if options['clear']:
            deleted, _ = Job.objects.all().delete()
            self.stdout.write(f'🗑️  {deleted} ofertas eliminadas')

        if not SEED_FILE.exists():
            self.stderr.write(self.style.ERROR(f'❌ No encontrado: {SEED_FILE}'))
            return

        with open(SEED_FILE, 'r', encoding='utf-8') as f:
            jobs_data = json.load(f)

        created = 0
        for job_data in jobs_data:
            _, is_new = Job.objects.get_or_create(
                external_id=job_data['external_id'],
                defaults={k: v for k, v in job_data.items() if k != 'external_id'}
            )
            if is_new:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f'✅ {created} ofertas cargadas de seed_jobs.json')
        )
