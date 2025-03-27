from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Occasion(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Expenditure(models.Model):
    occasion = models.ForeignKey('expenses.Occasion', on_delete=models.CASCADE, related_name='expenditures', null=True, blank=True)
    event_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenditures_paid')
    utilizers = models.ManyToManyField(User, related_name='expenditures_utilized')
    cleared = models.BooleanField(default=False)  # New field to track cleared status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} - {self.amount}"

class PaymentLog(models.Model):
    expenditure = models.ForeignKey(Expenditure, on_delete=models.CASCADE, related_name='payments')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    payee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} from {self.payer} to {self.payee}"
