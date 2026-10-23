from django.shortcuts import HttpResponse

# Create your views here.
def Saludo(request):
    return HttpResponse("Holita, bienvenido a TimeBank")