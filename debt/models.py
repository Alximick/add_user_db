from django.db import models

# Create your models here.
from django.conf import settings


class DebtType(models.Model):
    name = models.CharField(max_length=150)
    slung = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Debt(models.Model):
    type = models.ForeignKey(DebtType)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    year = models.IntegerField()
    month = models.IntegerField(null=True)
    amount = models.DecimalField(max_digits=1000, decimal_places=2, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.type

