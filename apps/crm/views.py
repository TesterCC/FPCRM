from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.


def index(request):
    return render(request, "index.html")


def customer_list(request):
    return render(request, "sales/customers.html")


class IndexView(View):

    def get(self, request):
        return render(request, "index.html", {})


class CustomerListView(View):

    def get(self, request):
        return render(request, "sales/customers.html", {})

