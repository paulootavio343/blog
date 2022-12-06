from django.forms import ModelForm
from .models import Comentaries
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = Comentaries
        fields = ('name', 'email', 'title', 'message')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control mb-2',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-2',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }
