from django.db import models

class Rental(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}-{self.id}"