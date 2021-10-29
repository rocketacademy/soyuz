from rest_framework import serializers

from .models import Batch, Section


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ("id", "start_date", "created_at", "updated_at")


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ("id", "name", "batch", "created_at", "updated_at")
