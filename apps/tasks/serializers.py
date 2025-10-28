from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    created_at_formatted = serializers.SerializerMethodField()
    updated_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'created_at',
            'created_at_formatted',
            'updated_at',
            'updated_at_formatted',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_created_at_formatted(self, obj):

        return obj.created_at.strftime('%d/%m/%Y %H:%M')

    def get_updated_at_formatted(self, obj):

        return obj.updated_at.strftime('%d/%m/%Y %H:%M')

    def validate_title(self, value):

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El título debe tener al menos 3 caracteres."
            )
        return value.strip()


class TaskListSerializer(serializers.ModelSerializer):


    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'created_at_formatted',
        ]

    def get_created_at_formatted(self, obj):

        return obj.created_at.strftime('%d/%m/%Y %H:%M')


class TaskToggleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'completed']
        read_only_fields = ['id']