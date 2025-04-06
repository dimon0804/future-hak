from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'status', 'content', 'image', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }