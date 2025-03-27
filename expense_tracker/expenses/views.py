from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Occasion, Expenditure
from .serializers import OccasionSerializer, ExpenditureSerializer, ClearExpenseSerializer, OccasionSummarySerializer


class OccasionCreateView(generics.CreateAPIView):
    queryset = Occasion.objects.all()
    serializer_class = OccasionSerializer


class ExpenditureCreateView(generics.CreateAPIView):
    queryset = Expenditure.objects.all()
    serializer_class = ExpenditureSerializer


class ClearExpenseView(generics.GenericAPIView):
    serializer_class = ClearExpenseSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            payment_log = serializer.save()
            return Response({
                "message": "Expense cleared successfully.",
                "payment_log": {
                    "id": payment_log.id,
                    "payer": payment_log.payer.username,
                    "payee": payment_log.payee.username,
                    "amount": payment_log.amount,
                    "timestamp": payment_log.timestamp
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OccasionExpenditureSummaryView(generics.RetrieveAPIView):
    queryset = Occasion.objects.all()
    serializer_class = OccasionSummarySerializer

    def get(self, request, *args, **kwargs):
        occasion_id = kwargs.get('pk')
        try:
            occasion = self.queryset.get(pk=occasion_id)
            serializer = self.get_serializer(occasion)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Occasion.DoesNotExist:
            return Response({"error": "Occasion not found."}, status=status.HTTP_404_NOT_FOUND)  # Custom error response
