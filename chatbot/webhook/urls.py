from django.urls import path
from .views import Webhook

urlpatterns = [
    path("", Webhook.as_view(), name="webhook"),
]