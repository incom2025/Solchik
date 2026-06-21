from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .forms import OrderRequestForm, ReviewForm
from .models import Product, ProductInstance, OrderRequest, Review
from .services import sentiment_analysis, detect_tags, send_telegram_order

class HomePageView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['product_count'] = Product.objects.count()
        ctx['available_count'] = ProductInstance.objects.filter(status='available').count()
        ctx['order_count'] = OrderRequest.objects.count()
        return ctx

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['order_form'] = OrderRequestForm(initial={
            'product': self.object,
            'source': self.request.GET.get('source', 'website'),
            'utm_source': self.request.GET.get('utm_source', ''),
            'utm_campaign': self.request.GET.get('utm_campaign', ''),
            'utm_content': self.request.GET.get('utm_content', ''),
        })
        ctx['review_form'] = ReviewForm(initial={'product': self.object})
        ctx['similar'] = Product.objects.exclude(id=self.object.id)[:4]
        return ctx

class OrderCreateView(CreateView):
    model = OrderRequest
    form_class = OrderRequestForm
    template_name = 'catalog/order_form.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.product:
            self.object.product.order_clicks += 1
            self.object.product.save(update_fields=['order_clicks'])
        send_telegram_order(self.object)
        messages.success(self.request, 'Заявку збережено та передано адміністратору.')
        return response

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        review = form.save(commit=False)
        label, score = sentiment_analysis(review.text)
        review.sentiment_label = label
        review.sentiment_score = score
        review.save()
        product = review.product
        reviews = product.reviews.all()
        product.sentiment_score = sum(r.sentiment_score for r in reviews) / max(reviews.count(), 1)
        product.tags = detect_tags(product.title + ' ' + product.description + ' ' + review.text)
        product.save(update_fields=['sentiment_score', 'tags'])
        return redirect(product.get_absolute_url())

class MyBookedProductsView(LoginRequiredMixin, ListView):
    model = ProductInstance
    template_name = 'catalog/my_booked.html'
    context_object_name = 'instances'

    def get_queryset(self):
        return ProductInstance.objects.filter(user=self.request.user)

class ThanksView(TemplateView):
    template_name = 'catalog/thanks.html'
