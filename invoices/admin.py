from django.contrib import admin
from .models import Invoice, InvoiceLine, Payment


# Register your models here.



admin.site.register(Invoice)
admin.site.register(InvoiceLine)
admin.site.register(Payment)