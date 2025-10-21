from django.db import models

class Pais(models.Model):
    id_Pais = models.AutoField(primary_key=True)
    Codigo = models.IntegerField('Código', null=True, blank=True)
    iso3166a1 = models.CharField('ISO 3166-1', max_length=2, null=True, blank=True)
    iso3166a2 = models.CharField('ISO 3166-2', max_length=5, null=True, blank=True)
    Pais = models.CharField('País', max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'paises'
        verbose_name = 'País'
        verbose_name_plural = 'Países'

    def __str__(self):
        return self.Pais if self.Pais else ''
