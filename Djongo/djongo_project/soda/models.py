from django.db import models

class Soda(models.Model):
    _id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=2, decimal_places=2)

    class Meta:
        ordering = ('_id',)
