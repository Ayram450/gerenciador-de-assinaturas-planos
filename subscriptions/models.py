from django.db import models


class Subscription(models.Model):
    nomePlano = models.CharField(max_length=100, null=False, blank=False)
    empresa = models.CharField(max_length=100, null=False, blank=False)
    data_venc = models.DateTimeField(null=False, blank=False)
    categoria = models.CharField(max_length=50, null=False, blank=False)
    valorMens = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, blank=False
    )


