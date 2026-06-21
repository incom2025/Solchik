from django.shortcuts import render

from django.views.generic import ListView
from .models import Imagess


class HomePageView(ListView):
    model = Imagess
    template_name = "home.html"

from django.views.generic import ListView, CreateView  # new
from django.urls import reverse_lazy  # new

from .forms import ImagessForm  # new
from .models import Imagess

class HomePageView(ListView):
    model = Imagess
    template_name = "home.html"

class CreateImagessView(CreateView):  # new
    model = Imagess
    form_class = ImagessForm
    template_name = "imagess.html"
    success_url = reverse_lazy("home")

