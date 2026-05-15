from django.contrib import admin
from .models import Job, ScraperRun


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display  = ['title', 'company', 'source', 'remote', 'date_posted', 'fetched_at']
    list_filter   = ['source', 'remote', 'date_posted']
    search_fields = ['title', 'company', 'location', 'description']
    readonly_fields = ['external_id', 'fetched_at', 'updated_at']
    ordering      = ['-date_posted', '-fetched_at']
    list_per_page = 50


@admin.register(ScraperRun)
class ScraperRunAdmin(admin.ModelAdmin):
    list_display  = ['source', 'status', 'jobs_found', 'jobs_new', 'started_at', 'finished_at']
    list_filter   = ['source', 'status']
    readonly_fields = ['started_at', 'finished_at', 'jobs_found', 'jobs_new', 'error_msg']
    ordering      = ['-started_at']
