from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Loko(models.Model):
    seria = models.CharField(max_length=255, unique=True)
    stavka_za_km = models.FloatField()

    def __str__(self):
        return self.seria


class Filial(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Probeg(models.Model):
    filial = models.ForeignKey(Filial,
                               on_delete=models.CASCADE)
    loko = models.ForeignKey(Loko,
                             on_delete=models.CASCADE)
    km_count = models.FloatField()

    year = models.PositiveIntegerField(validators=[MinValueValidator(1851),MaxValueValidator(9999)])

    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        unique_together = ('filial', 'loko', 'year')