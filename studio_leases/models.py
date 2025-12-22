import calendar
from datetime import date

from django.db import models
from studio_profiles.models import Horse, Owner, Trainer


class Lease(models.Model):
    class Status(models.TextChoices):
        PROPOSED = "PROPOSED", "Proposed"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PROPOSED,
    )
    horse = models.ForeignKey(Horse, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.PROTECT)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    syndicate_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Will auto-populate as '[Horse Name] Syndicate'",
    )
    start_date = models.DateField()
    lease_months = models.IntegerField(default=12)
    revenue_share = models.DecimalField(max_digits=5, decimal_places=2, default=80.00)

    def __str__(self):
        return f"{self.syndicate_name} ({self.horse.name})"
