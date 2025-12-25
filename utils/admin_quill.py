from django import forms
from django.utils.safestring import mark_safe


class QuillWidget(forms.Textarea):

    class Media:
        css = {
            'all': ('https://cdn.quilljs.com/1.3.6/quill.snow.css',)
        }
        js = (
            'https://cdn.quilljs.com/1.3.6/quill.min.js',
        )
    def render(self, name, value, attrs=None, renderer=None):
        textarea_html = super().render(name, value, attrs, renderer)
        quill_js = f"""
            <script>
            document.addEventListener("DOMContentLoaded", function() {{
                var textarea = document.getElementById("{attrs['id']}");
                if (!textarea) return;

                var wrapper = document.createElement('div');
                wrapper.style.width = "600px";  // Set desired width here
                wrapper.style.margin = "20px";  // Set desired margin here
                wrapper.style.height = "300px";  // Set desired height here

                textarea.parentNode.insertBefore(wrapper, textarea);
                textarea.style.display = 'none';

                var quillContainer = document.createElement('div');
                wrapper.appendChild(quillContainer);

                var quill = new Quill(quillContainer, {{
                    theme: 'snow',
                    modules: {{
                        toolbar: [
                            [{{ 'font': [] }}],
                            [{{ 'header': [1, 2, 3, false] }}],
                            ['bold', 'italic', 'underline', 'strike'],
                            ['blockquote', 'code-block'],
                            [{{ 'list': 'ordered' }}, {{ 'list': 'bullet' }}],
                            [{{ 'script': 'sub' }}, {{ 'script': 'super' }}],
                            [{{ 'indent': '-1' }}, {{ 'indent': '+1' }}],
                            [{{ 'direction': 'rtl' }}],
                            [{{ 'color': [] }}, {{ 'background': [] }}],
                            [{{ 'align': [] }}],
                            ['link'],
                            ['clean']
                        ]
                    }}
                }});

                // Force toolbar and editor to stack vertically
                var toolbar = wrapper.querySelector('.ql-toolbar');
                var editor = wrapper.querySelector('.ql-container');
                if(toolbar) toolbar.style.display = 'block';
                if(editor) editor.style.display = 'block';

                quill.root.innerHTML = textarea.value || '';

                quill.on('text-change', function() {{
                    textarea.value = quill.root.innerHTML;
                }});
            }});
            </script>
            """
        return mark_safe(textarea_html + quill_js)