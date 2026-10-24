from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Risk(models.Model):
    CATEGORY_CHOICES = [
        ("Cyber", "Cyber"),
        ("Operational", "Operational"),
        ("Financial", "Financial"),
        ("Compliance", "Compliance"),
        ("Third-party", "Third-party"),
    ]
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Mitigated", "Mitigated"),
        ("Closed", "Closed"),
    ]
    LEVEL_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    risk_id = models.CharField(max_length=20, unique=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    owner = models.CharField(max_length=100)
    likelihood = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    impact = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    risk_score = models.PositiveSmallIntegerField(default=1, editable=False)
    risk_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="Low", editable=False)
    mitigation_plan = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    date_identified = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="created_risks"
    )

    def save(self, *args, **kwargs):
        if not 1 <= self.likelihood <= 5:
            raise ValueError("Likelihood must be between 1 and 5.")
        if not 1 <= self.impact <= 5:
            raise ValueError("Impact must be between 1 and 5.")

        self.risk_score = self.likelihood * self.impact
        if self.risk_score >= 20:
            self.risk_level = "Critical"
        elif self.risk_score >= 12:
            self.risk_level = "High"
        elif self.risk_score >= 6:
            self.risk_level = "Medium"
        else:
            self.risk_level = "Low"

        if not self.risk_id:
            # Simple ID for a small classroom project. Unique constraint protects duplicates.
            last = Risk.objects.order_by("-id").first()
            next_number = (last.id + 1) if last else 1
            self.risk_id = f"R-{next_number:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.risk_id} - {self.title}"

    class Meta:
        ordering = ["-risk_score", "risk_id"]
