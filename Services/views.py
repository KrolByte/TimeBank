#from django.shortcuts import HttpResponse
from django.shortcuts import render
from .models import ServiceOffer, Exchange, Benefit

# Create your views here.
#def Saludo(request):
 #   return HttpResponse("Holita, bienvenido a TimeBank")

def index(request):
    offers_list = ServiceOffer.objects.all()
    return render(request, "index.html", {"ofertas": offers_list})


def exchanges(request):
    exchanges_list = Exchange.objects.all()
    return render(
        request, "exchanges.html", {"exchanges": exchanges_list}
    )


def benefits(request):
    benefits_list = Benefit.objects.all()
    return render(request, "benefits.html", {"benefits": benefits_list})