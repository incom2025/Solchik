import csv
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.views.generic import TemplateView
from catalog.models import Product, OrderRequest, Review

class DashboardView(TemplateView):
    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['orders_total'] = OrderRequest.objects.count()
        ctx['revenue_total'] = OrderRequest.objects.aggregate(s=Sum('amount'))['s'] or 0
        ctx['products'] = Product.objects.order_by('-views')[:10]
        ctx['sentiment'] = Review.objects.values('sentiment_label').annotate(c=Count('id'))
        ctx['traffic'] = OrderRequest.objects.values('utm_source').annotate(c=Count('id')).order_by('-c')
        return ctx

def export_orders_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="solchik_orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['created_at', 'name', 'phone', 'product', 'amount', 'source', 'utm_source', 'utm_campaign'])
    for o in OrderRequest.objects.select_related('product'):
        writer.writerow([o.created_at, o.name, o.phone, o.product.title if o.product else '', o.amount, o.source, o.utm_source, o.utm_campaign])
    return response
