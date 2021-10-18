from django.db.models import fields
from rest_framework.fields import ReadOnlyField
from .models import Estacionamiento, Comuna
from rest_framework import serializers

class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = '__all__'


class EstacionamientoSerializer(serializers.ModelSerializer):
    nombre_comuna = serializers.CharField(read_only=True, source="comuna.nombre")
    comuna = ComunaSerializer(read_only=True)
    comuna_id = serializers.PrimaryKeyRelatedField(queryset=Comuna.objects.all(), source="comuna")
    nombre = serializers.CharField(required=True)

    def validate_nombre(self, value):
        existe = Estacionamiento.objects.filter(nombre__iexact=value).exists()

        if existe:
            raise serializers.ValidationError("Este estacionamiento ya existe")

        return value


    class Meta:
        model = Estacionamiento
        fields = '__all__'