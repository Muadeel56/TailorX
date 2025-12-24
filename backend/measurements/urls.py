from django.urls import path
from .views import (
    MeasurementTemplateListView,
    MeasurementTemplateDetailView,
    CustomerMeasurementListView,
    CustomerMeasurementDetailView
)

app_name = 'measurements'

urlpatterns = [
    # Template endpoints (public)
    path('templates/', MeasurementTemplateListView.as_view(), name='template-list'),
    path('templates/<int:id>/', MeasurementTemplateDetailView.as_view(), name='template-detail'),

    # Customer measurement endpoints (authenticated)
    path('', CustomerMeasurementListView.as_view(), name='measurement-list'),
    path('<int:id>/', CustomerMeasurementDetailView.as_view(), name='measurement-detail'),
]

