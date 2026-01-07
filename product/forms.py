from django import forms

from utils.admin_quill import QuillWidget
from .models import Category, Product


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "description": QuillWidget(attrs={"class": "quill-editor"}),
        }


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "description": QuillWidget(attrs={"class": "quill-editor"}),
        }
