from rest_framework import serializers, generics, status
from .models import Expenditure, Occasion, PaymentLog
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

User = get_user_model()

class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = ['id', 'name', 'date', 'description']

class ExpenditureSerializer(serializers.ModelSerializer):
    expender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    utilizers = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Expenditure
        fields = ['id', 'occasion', 'event_name', 'amount', 'expender', 'utilizers', 'created_at']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_utilizers(self, value):
        if not value:
            raise serializers.ValidationError("At least one utilizer must be provided.")
        return value

class ClearExpenseSerializer(serializers.Serializer):
    expenditure_id = serializers.IntegerField()
    payer_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        try:
            expenditure = Expenditure.objects.get(id=data['expenditure_id'])
        except Expenditure.DoesNotExist:
            raise serializers.ValidationError("Expenditure does not exist.")

        if expenditure.cleared:
            raise serializers.ValidationError("This expense has already been cleared.")

        if data['amount'] != expenditure.amount:
            raise serializers.ValidationError("The payment amount must match the expenditure amount.")

        if data['payer_id'] not in expenditure.utilizers.values_list('id', flat=True):
            raise serializers.ValidationError("The payer must be one of the utilizers.")

        return data

    def create(self, validated_data):
        expenditure = Expenditure.objects.get(id=validated_data['expenditure_id'])
        payer = User.objects.get(id=validated_data['payer_id'])
        payee = expenditure.expender

        # Create a payment log
        payment_log = PaymentLog.objects.create(
            expenditure=expenditure,
            payer=payer,
            payee=payee,
            amount=validated_data['amount']
        )

        # Mark the expenditure as cleared
        expenditure.cleared = True
        expenditure.save()

        return payment_log

class ExpenditureSummarySerializer(serializers.ModelSerializer):
    expender = serializers.StringRelatedField()
    utilizers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Expenditure
        fields = ['id', 'event_name', 'amount', 'expender', 'utilizers', 'cleared', 'created_at']


class OccasionSummarySerializer(serializers.ModelSerializer):
    expenditures = ExpenditureSummarySerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Occasion
        fields = ['id', 'name', 'date', 'description', 'total_amount', 'expenditures']

    def get_total_amount(self, obj):
        return sum(expenditure.amount for expenditure in obj.expenditures.all())

class OccasionExpenditureSummaryView(generics.RetrieveAPIView):
    queryset = Occasion.objects.all()
    serializer_class = OccasionSummarySerializer

    def get(self, request, *args, **kwargs):
        try:
            occasion = self.get_object()
            serializer = self.get_serializer(occasion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Occasion.DoesNotExist:
            raise NotFound({"error": "Occasion not found."})  # Custom error response