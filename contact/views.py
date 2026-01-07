from rest_framework import generics, permissions

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactMessageSerializer
    queryset = ContactMessage.objects.all()
