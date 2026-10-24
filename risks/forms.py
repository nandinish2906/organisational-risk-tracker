from django import forms
from .models import Risk


class RiskForm(forms.ModelForm):
    class Meta:
        model = Risk
        fields = [
            "title", "description", "category", "owner",
            "likelihood", "impact", "mitigation_plan", "status",
            "date_identified", "due_date",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "mitigation_plan": forms.Textarea(attrs={"rows": 3}),
            "date_identified": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "likelihood": forms.Select(),
            "impact": forms.Select(),
        }

    def clean(self):
        cleaned = super().clean()
        likelihood = cleaned.get("likelihood")
        impact = cleaned.get("impact")
        if likelihood is not None and not 1 <= likelihood <= 5:
            self.add_error("likelihood", "Choose a value from 1 to 5.")
        if impact is not None and not 1 <= impact <= 5:
            self.add_error("impact", "Choose a value from 1 to 5.")
        return cleaned
