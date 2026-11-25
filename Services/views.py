#from django.shortcuts import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ServiceOfferForm, StudentRegistrationForm
from .models import ServiceOffer, Exchange, Benefit, UserProfile

# Create your views here.
#def Saludo(request):
 #   return HttpResponse("Holita, bienvenido a TimeBank")

def register_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            UserProfile.objects.create(
                user=new_user,
                student_id=form.cleaned_data["student_id"],
                phone=form.cleaned_data["phone"],
                purpose=form.cleaned_data["purpose"],
                hours_balance=4,
                accumulated_hours=0,
            )
            login(request, new_user)
            return redirect("index")
    else:
        form = StudentRegistrationForm()
    return render(request, "register.html", {"form": form})

def index(request):
    offers_list = ServiceOffer.objects.all()
    return render(request, "index.html", {"offers": offers_list})

def offer_detail(request, pk):
    offer = get_object_or_404(ServiceOffer, pk=pk)
    return render(request, "offer_detail.html", {"offer": offer})

@login_required
def create_offer(request):
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "student_id": "ADMIN",
            "phone": "0000000000",
            "accumulated_hours": 0,
        },
    )
    if request.method == "POST":
        form = ServiceOfferForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = ServiceOfferForm()
    return render(request, "offer_form.html", {"form": form})

@login_required
def exchanges(request):
    exchanges_list = Exchange.objects.all()
    return render(
        request, "exchanges.html", {"exchanges": exchanges_list}
    )

@login_required
def benefits(request):
    benefits_list = Benefit.objects.all()
    return render(request, "benefits.html", {"benefits": benefits_list})