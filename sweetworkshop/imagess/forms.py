from django import forms
from .models import Imagess

class ImagessForm(forms.ModelForm):

    class Meta:
        model = Imagess
        fields = ["title", "cover"]
