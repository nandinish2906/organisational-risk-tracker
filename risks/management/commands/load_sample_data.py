from datetime import date, timedelta
from django.core.management.base import BaseCommand
from risks.models import Risk


SAMPLES = [
    ("R-001", "Phishing attack", "Cyber", 4, 5, "Train staff and enable email filtering; report suspicious messages.", "Open"),
    ("R-002", "Weak employee passwords", "Cyber", 4, 4, "Enforce strong passwords and multi-factor authentication.", "In Progress"),
    ("R-003", "Unpatched server", "Cyber", 3, 5, "Maintain a patch schedule and verify critical updates.", "Open"),
    ("R-004", "Missing data backups", "Operational", 4, 4, "Automate backups and test restoration regularly.", "Mitigated"),
    ("R-005", "Third-party service outage", "Third-party", 3, 4, "Document vendor escalation and continuity arrangements.", "In Progress"),
    ("R-006", "Lost company laptop", "Cyber", 3, 4, "Enable disk encryption and remote device management.", "Open"),
    ("R-007", "Unauthorised account access", "Cyber", 3, 5, "Review access rights and enable multi-factor authentication.", "Open"),
    ("R-008", "Regulatory deadline missed", "Compliance", 2, 5, "Use a compliance calendar and assign a responsible owner.", "In Progress"),
    ("R-009", "Knowledge lost when employee leaves", "Operational", 3, 3, "Maintain procedures and cross-train team members.", "Mitigated"),
    ("R-010", "Equipment failure", "Operational", 2, 4, "Schedule maintenance and keep critical spares.", "Open"),
    ("R-011", "Budget overrun", "Financial", 3, 3, "Review spending monthly and approve changes.", "In Progress"),
    ("R-012", "Website downtime", "Operational", 2, 4, "Monitor uptime and document recovery steps.", "Open"),
    ("R-013", "Sensitive email sent to wrong person", "Cyber", 2, 4, "Use recipient checks and data-loss prevention where available.", "Mitigated"),
    ("R-014", "Incomplete vendor security review", "Third-party", 2, 4, "Review vendor security evidence before renewal.", "Open"),
    ("R-015", "Unauthorised software installation", "Cyber", 3, 3, "Restrict installation permissions and maintain an approved list.", "In Progress"),
    ("R-016", "Expired software licence", "Compliance", 2, 2, "Track licence renewals in a central calendar.", "Closed"),
    ("R-017", "Printer malfunction", "Operational", 1, 2, "Maintain equipment and keep a support contact.", "Closed"),
    ("R-018", "Delayed invoice processing", "Financial", 2, 2, "Set processing deadlines and assign a backup approver.", "Mitigated"),
]


class Command(BaseCommand):
    help = "Load fictional sample risks for demonstration. Existing sample IDs are updated."

    def handle(self, *args, **options):
        today = date.today()
        for index, item in enumerate(SAMPLES):
            risk_id, title, category, likelihood, impact, mitigation, status = item
            Risk.objects.update_or_create(
                risk_id=risk_id,
                defaults={
                    "title": title,
                    "description": f"Sample scenario for demonstration: {title.lower()} could affect organisational operations or security.",
                    "category": category,
                    "owner": ["IT Team", "Security Team", "Operations Team"][index % 3],
                    "likelihood": likelihood,
                    "impact": impact,
                    "mitigation_plan": mitigation,
                    "status": status,
                    "date_identified": today - timedelta(days=(index + 1) * 3),
                    "due_date": today + timedelta(days=(index - 5) * 4) if index % 4 != 0 else None,
                },
            )
        self.stdout.write(self.style.SUCCESS(f"Loaded or updated {len(SAMPLES)} sample risks."))
