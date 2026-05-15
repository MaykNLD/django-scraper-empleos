from django.db import models


class Job(models.Model):
    """
    Oferta de trabajo scrapeada/importada de APIs públicas.
    """
    SOURCE_CHOICES = [
        ('arbeitnow', 'Arbeitnow'),
        ('remotive', 'Remotive'),
        ('seed', 'Seed Data'),
    ]

    # Identificación
    external_id = models.CharField(max_length=255, unique=True, db_index=True)
    source      = models.CharField(max_length=50, choices=SOURCE_CHOICES, db_index=True)

    # Datos de la oferta
    title       = models.CharField(max_length=500)
    company     = models.CharField(max_length=255, db_index=True)
    location    = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    tags        = models.JSONField(default=list, blank=True)
    salary      = models.CharField(max_length=100, blank=True)
    url         = models.URLField(max_length=1000, blank=True)
    remote      = models.BooleanField(default=False, db_index=True)

    # Fechas
    date_posted = models.DateField(null=True, blank=True, db_index=True)
    fetched_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name      = 'Oferta de trabajo'
        verbose_name_plural = 'Ofertas de trabajo'
        ordering          = ['-date_posted', '-fetched_at']
        indexes           = [
            models.Index(fields=['source', 'remote']),
            models.Index(fields=['date_posted', 'source']),
        ]

    def __str__(self):
        return f"{self.title} @ {self.company} ({self.source})"

    @property
    def skills_detected(self) -> list[str]:
        """Retorna skills detectados en descripción y tags."""
        return self.tags if self.tags else []


class ScraperRun(models.Model):
    """
    Registro de cada ejecución del scraper. Útil para auditoría y debug.
    """
    STATUS_CHOICES = [
        ('running', 'En ejecución'),
        ('success', 'Completado'),
        ('error',   'Error'),
    ]

    source      = models.CharField(max_length=50)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    jobs_found  = models.IntegerField(default=0)
    jobs_new    = models.IntegerField(default=0)
    error_msg   = models.TextField(blank=True)
    started_at  = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name        = 'Ejecución del scraper'
        verbose_name_plural = 'Ejecuciones del scraper'
        ordering            = ['-started_at']

    def __str__(self):
        return f"{self.source} | {self.status} | {self.started_at:%Y-%m-%d %H:%M}"

    def duration_seconds(self):
        if self.finished_at:
            return (self.finished_at - self.started_at).seconds
        return None
