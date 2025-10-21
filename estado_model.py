from django.db import models

class Estado(models.Model):
    id_Estado = models.AutoField(primary_key=True)
    Estado = models.CharField('Estado', max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'estados'
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['Estado']

    def __str__(self):
        return self.Estado if self.Estado else ''
