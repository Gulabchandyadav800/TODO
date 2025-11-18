from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    due_date = serializers.CharField(allow_null=True, required=False)  # Accept ISO string
    status = serializers.ChoiceField(choices=['pending', 'in_progress', 'done'], default='pending')
