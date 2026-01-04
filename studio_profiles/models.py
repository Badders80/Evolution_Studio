from django.db import models


class Trainer(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Owner(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Horse(models.Model):
    name = models.CharField(max_length=255)
    microchip = models.CharField(max_length=50, primary_key=True)
    sex = models.CharField(max_length=20, default="Gelding")
    nztr_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

