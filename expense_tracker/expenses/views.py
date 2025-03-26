from django.shortcuts import render
from rest_framework import generics
from .models import Occasion
from .serializers import OccasionSerializer


class OccasionCreateView(generics.CreateAPIView):
    queryset = Occasion.objects.all()
    serializer_class = OccasionSerializer
