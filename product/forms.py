from django import forms

from utils.admin_quill import QuillWidget
from .models import Category


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": QuillWidget(attrs={"class": "quill-editor"}),
        }
