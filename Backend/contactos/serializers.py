from rest_framework import serializers
from .models import Contacto
import re

class ContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'

    def validate_celular(self, value):
        # Elimina todos los espacios y otros caracteres no numéricos
        cleaned = re.sub(r'\D', '', value)
        
        # Revisa si ya existe otro contacto con ese número limpio
        if Contacto.objects.filter(celular=cleaned).exists():
            raise serializers.ValidationError("Este número de celular ya está registrado.")
        
        return cleaned