from rest_framework import serializers
from .models import Sensor, Measurement

class MeasurementSerializer(serializers.ModelSerializer):
    sensor = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all())
    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'created_at', 'image']

class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']