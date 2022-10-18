from django.forms import ModelForm
from .models import Comentaries


class CommentForm(ModelForm):
    class Meta:
        model = Comentaries
        fields = ('name', 'email', 'title', 'message')
