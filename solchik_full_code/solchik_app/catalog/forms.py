from django import forms
from .models import Product, OrderRequest, Review

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'description', 'weight', 'price', 'image', 'filings', 'vyrib']

class OrderRequestForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = ['product', 'name', 'phone', 'message', 'source', 'utm_source', 'utm_campaign', 'utm_content', 'amount']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
            'product': forms.HiddenInput(),
            'source': forms.HiddenInput(),
            'utm_source': forms.HiddenInput(),
            'utm_campaign': forms.HiddenInput(),
            'utm_content': forms.HiddenInput(),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'text']
