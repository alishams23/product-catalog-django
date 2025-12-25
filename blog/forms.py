from django import forms
from utils.admin_quill import QuillWidget
from .models import Blog


class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
        widgets = {
            "body": QuillWidget(attrs={'class': 'quill-editor'}),
        }
