from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("risks/", views.risk_list, name="risk_list"),
    path("risks/add/", views.risk_create, name="risk_create"),
    path("risks/<int:pk>/", views.risk_detail, name="risk_detail"),
    path("risks/<int:pk>/edit/", views.risk_update, name="risk_update"),
    path("risks/<int:pk>/delete/", views.risk_delete, name="risk_delete"),
    path("reports/export.csv", views.export_csv, name="export_csv"),
]
