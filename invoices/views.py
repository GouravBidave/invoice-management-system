from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice, Payment
from .serializers import InvoiceSerializer


@api_view(['GET'])
def get_invoice(request, id):
    try:
        invoice = Invoice.objects.get(id=id)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=404)

    serializer = InvoiceSerializer(invoice)
    return Response(serializer.data)


@api_view(['POST'])
def add_payment(request, id):
    try:
        invoice = Invoice.objects.get(id=id)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=404)

    amount = request.data.get("amount")

    try:
        Payment.objects.create(invoice=invoice, amount=amount)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    return Response({"message": "Payment added successfully"})


@api_view(['POST'])
def archive_invoice(request):
    invoice_id = request.data.get("id")

    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=404)

    invoice.isArchived = True
    invoice.save()

    return Response({"message": "Invoice archived"})


@api_view(['POST'])
def restore_invoice(request):
    invoice_id = request.data.get("id")

    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found"}, status=404)

    invoice.isArchived = False
    invoice.save()

    return Response({"message": "Invoice restored"})