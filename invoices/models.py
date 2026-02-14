from django.db import models


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PAID', 'Paid'),
    ]

    invoiceNumber = models.CharField(max_length=50)
    customerName = models.CharField(max_length=100)
    issueDate = models.DateField()
    dueDate = models.DateField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amountPaid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balanceDue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    isArchived = models.BooleanField(default=False)

    def update_totals(self):
        total = sum(line.lineTotal for line in self.lines.all())
        paid = sum(payment.amount for payment in self.payments.all())

        self.total = total
        self.amountPaid = paid
        self.balanceDue = total - paid

        if self.balanceDue <= 0 and total > 0:
            self.status = "PAID"
        else:
            self.status = "DRAFT"

        self.save(update_fields=["total", "amountPaid", "balanceDue", "status"])


class InvoiceLine(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="lines", on_delete=models.CASCADE)

    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    lineTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.lineTotal = self.quantity * self.unitPrice
        super().save(*args, **kwargs)
        self.invoice.update_totals()

    def delete(self, *args, **kwargs):
        invoice = self.invoice
        super().delete(*args, **kwargs)
        invoice.update_totals()


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="payments", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymentDate = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise ValueError("Payment must be greater than 0")

        if self.amount > self.invoice.balanceDue:
            raise ValueError("Overpayment not allowed")

        super().save(*args, **kwargs)
        self.invoice.update_totals()