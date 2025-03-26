from django.db import models

class Occasion(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
