from django.urls import path
from .views import CheckOnlineView, TokenGenerateView

urlpatterns = [
    path('check-online/', CheckOnlineView.as_view(), name='check-online'),
    path('generate-token/', TokenGenerateView.as_view(), name='generate-token'),
]
