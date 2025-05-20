from django.db import models
from django.core.exceptions import ValidationError

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    numero_celular = models.CharField(max_length=15, unique=True)
    correo = models.EmailField()

    def clean(self):
        if Contacto.objects.exclude(pk=self.pk).filter(
            numero_celular=self.numero_celular
        ).exclude(nombre=self.nombre, apellido=self.apellido).exists():
            raise ValidationError("Este número de celular ya está registrado para otro contacto.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"