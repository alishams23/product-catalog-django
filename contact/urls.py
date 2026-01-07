from django.urls import path

from .views import ContactMessageCreateAPIView

app_name = "contact"

urlpatterns = [
    path("", ContactMessageCreateAPIView.as_view(), name="contact-create"),
]
