from rest_framework import serializers

class SkillSerializer(serializers.Serializer):
    company = serializers.CharField()
    employee = serializers.ListField(child=serializers.CharField())

