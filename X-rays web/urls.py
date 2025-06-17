from django.urls import path
from . import views

urlpatterns = [
    path('patients/<int:id>/', views.patient_detail, name='patient_detail'),
    # Các URL khác...
]
