from django.shortcuts import render

# Create your views here.
from .models import Product, Vyrib, ProductInstance, Filing

def index(request):
    """
    Функція відображення для домашньої сторінки сайту.

    """
    # Генерація "кількості" деяких основних об'єктів
    num_product= Product.objects.all().count()
    num_instances= ProductInstance.objects.all().count()
    # Доступні продукти (статус = 'a')
    num_instances_available= ProductInstance.objects.filter(status__exact='a').count()
    num_vyrib = Vyrib.objects.count()  # Метод 'all()' застосовоний по замовчуванню.
    # Number of visits to this view, як counted в session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Кількість відвідувань цього перегляду, яка підрахована у змінній сесії.
    return render(
        request,
        'index.html',
        context={'num_product':num_product,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_vyrib':num_vyrib,'num_visits':num_visits}, # num_visits appended
    )
    # Відображення HTML-шаблону index.html з даними всередині
    # змінної контексту context
    return render(
        request,
        'index.html',
        context={'num_products ':num_products,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_vyrib ':num_vyrib },
    )
from django.views import generic

class ProductDetailView(generic.DetailView):
    model = Product
class ProductListView(generic.ListView):
    model = Product
    paginate_by = 4
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedProductByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Загальний продукт із переліком переглядів на основі класу, наданий поточному користувачеві.
    """
    model = ProductInstance
    template_name ='catalog/productinstance_list_booked_user.html'
    paginate_by = 10

    def get_queryset(self):
        return ProductInstance.objects.filter(booked=self.request.user).filter(status__exact='o').order_by('due_back')
