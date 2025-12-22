from django.urls import path
from .views import TailorListView, TailorDetailView, TailorPortfolioView

app_name = 'tailors'

urlpatterns = [
    path('', TailorListView.as_view(), name='tailor-list'),
    path('<int:id>/', TailorDetailView.as_view(), name='tailor-detail'),
    path('<int:id>/portfolio/', TailorPortfolioView.as_view(), name='tailor-portfolio'),
]

