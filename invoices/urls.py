from django.urls import path
from . import views

urlpatterns = [
    path('api/invoices/<int:id>/', views.get_invoice),
    path('api/invoices/<int:id>/payments/', views.add_payment),
    path('api/invoices/archive/', views.archive_invoice),
    path('api/invoices/restore/', views.restore_invoice),
    path('invoices/<int:id>/', views.invoice_detail_page),
]