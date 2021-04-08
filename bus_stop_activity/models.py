from django.db import models

# Create your models here.


class TrafficData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    a = models.FloatField()
    b = models.FloatField()

    def __str__(self):
        return str(self.created_at)