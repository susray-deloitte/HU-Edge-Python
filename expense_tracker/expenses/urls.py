from django.urls import path
from .views import OccasionCreateView

urlpatterns = [
    path('occasions/', OccasionCreateView.as_view(), name='occasion-create'),
]