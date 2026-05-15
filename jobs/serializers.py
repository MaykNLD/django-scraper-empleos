from rest_framework import serializers
from .models import Job, ScraperRun


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Job
        fields = [
            'id', 'external_id', 'source', 'title', 'company',
            'location', 'tags', 'salary', 'url', 'remote',
            'date_posted', 'fetched_at',
        ]
        read_only_fields = ['id', 'fetched_at']


class JobListSerializer(serializers.ModelSerializer):
    """Versión reducida para listados."""
    class Meta:
        model  = Job
        fields = ['id', 'title', 'company', 'location', 'remote', 'source', 'date_posted', 'url', 'tags']


class ScraperRunSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model  = ScraperRun
        fields = ['id', 'source', 'status', 'jobs_found', 'jobs_new', 'error_msg', 'started_at', 'finished_at', 'duration']

    def get_duration(self, obj):
        return obj.duration_seconds()
