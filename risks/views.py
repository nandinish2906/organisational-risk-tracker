import csv
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import RiskForm
from .models import Risk


@login_required
def dashboard(request):
    total = Risk.objects.count()
    open_count = Risk.objects.filter(status="Open").count()
    high_critical = Risk.objects.filter(risk_level__in=["High", "Critical"]).count()
    mitigated_count = Risk.objects.filter(status="Mitigated").count()
    mitigated_percent = round((mitigated_count / total) * 100) if total else 0

    level_rows = list(
        Risk.objects.values("risk_level").annotate(count=Count("id")).order_by("risk_level")
    )
    category_rows = list(
        Risk.objects.values("category").annotate(count=Count("id")).order_by("category")
    )
    status_rows = list(
        Risk.objects.values("status").annotate(count=Count("id")).order_by("status")
    )
    top_risks = Risk.objects.all()[:5]

    context = {
        "total": total,
        "open_count": open_count,
        "high_critical": high_critical,
        "mitigated_percent": mitigated_percent,
        "top_risks": top_risks,
        "level_labels": [r["risk_level"] for r in level_rows],
        "level_values": [r["count"] for r in level_rows],
        "category_labels": [r["category"] for r in category_rows],
        "category_values": [r["count"] for r in category_rows],
        "status_labels": [r["status"] for r in status_rows],
        "status_values": [r["count"] for r in status_rows],
    }
    return render(request, "risks/dashboard.html", context)


@login_required
def risk_list(request):
    risks = Risk.objects.all()
    search = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    status = request.GET.get("status", "")
    level = request.GET.get("level", "")

    if search:
        risks = risks.filter(
            Q(risk_id__icontains=search) |
            Q(title__icontains=search) |
            Q(owner__icontains=search)
        )
    if category:
        risks = risks.filter(category=category)
    if status:
        risks = risks.filter(status=status)
    if level:
        risks = risks.filter(risk_level=level)

    context = {
        "risks": risks,
        "search": search,
        "selected_category": category,
        "selected_status": status,
        "selected_level": level,
        "categories": Risk.CATEGORY_CHOICES,
        "statuses": Risk.STATUS_CHOICES,
        "levels": Risk.LEVEL_CHOICES,
    }
    return render(request, "risks/risk_list.html", context)


@login_required
def risk_create(request):
    if request.method == "POST":
        form = RiskForm(request.POST)
        if form.is_valid():
            risk = form.save(commit=False)
            risk.created_by = request.user
            risk.save()
            messages.success(request, f"{risk.risk_id} was created successfully.")
            return redirect("risk_detail", pk=risk.pk)
    else:
        form = RiskForm()
    return render(request, "risks/risk_form.html", {"form": form, "page_title": "Add a risk"})


@login_required
def risk_detail(request, pk):
    risk = get_object_or_404(Risk, pk=pk)
    return render(request, "risks/risk_detail.html", {"risk": risk})


@login_required
def risk_update(request, pk):
    risk = get_object_or_404(Risk, pk=pk)
    if request.method == "POST":
        form = RiskForm(request.POST, instance=risk)
        if form.is_valid():
            form.save()
            messages.success(request, f"{risk.risk_id} was updated successfully.")
            return redirect("risk_detail", pk=risk.pk)
    else:
        form = RiskForm(instance=risk)
    return render(request, "risks/risk_form.html", {
        "form": form, "page_title": f"Edit {risk.risk_id}", "risk": risk
    })


@login_required
@require_POST
def risk_delete(request, pk):
    risk = get_object_or_404(Risk, pk=pk)
    risk_id = risk.risk_id
    risk.delete()
    messages.success(request, f"{risk_id} was deleted.")
    return redirect("risk_list")


@login_required
def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="risk_register.csv"'
    writer = csv.writer(response)
    writer.writerow([
        "Risk ID", "Title", "Description", "Category", "Owner",
        "Likelihood", "Impact", "Score", "Level", "Mitigation Plan",
        "Status", "Date Identified", "Due Date",
    ])
    for r in Risk.objects.all():
        writer.writerow([
            r.risk_id, r.title, r.description, r.category, r.owner,
            r.likelihood, r.impact, r.risk_score, r.risk_level,
            r.mitigation_plan, r.status, r.date_identified, r.due_date or "",
        ])
    return response
