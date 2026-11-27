#from django.shortcuts import HttpResponse
import uuid
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ServiceOfferForm, StudentRegistrationForm, ExchangeRequestForm
from .models import ServiceOffer, Exchange, Benefit, UserProfile, Category, Schedule
from django.db.models import Q

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
            offer = form.save(commit=False)
            offer.offer_id = f"OF-{uuid.uuid4().hex[:6].upper()}" #upper es para que el hexadecimal esté en mayúsculas
            offer.provider = profile
            # Categoría existente o crear nueva
            selected_category = form.cleaned_data.get("category") #cleaned_data me trae los datos limpios y en el formato correcto
            new_cat_name = form.cleaned_data.get("new_category_name", "").strip() #strip elimina espacios en blanco, "" respaldo por si un campo no tiene info
            if selected_category:
                offer.category = selected_category
            elif new_cat_name:
                new_cat_desc = form.cleaned_data.get(
                    "new_category_description", ""
                ).strip()
                category_obj, _ = Category.objects.get_or_create(
                    name_category__iexact=new_cat_name, #busca el nombre de la categoría sin importar mayúsculas o minúsculas
                    defaults={
                        "category_id": f"CAT-{uuid.uuid4().hex[:6].upper()}",
                        "name_category": new_cat_name,
                        "description_category": new_cat_desc,
                    },
                )
                offer.category = category_obj
            offer.save()
            #Guarda disponibilidad horaria si fue completada
            day = form.cleaned_data.get("days_week")
            start = form.cleaned_data.get("start_hour")
            end = form.cleaned_data.get("end_hour")
            if day and start and end:
                Schedule.objects.create(
                    schedule_id=f"SCH-{uuid.uuid4().hex[:5].upper()}",
                    days_week=day,
                    start_hour=start,
                    end_hour=end,
                    offer=offer,
                )
            return redirect("offer_detail", pk=offer.pk)
    else:
        form = ServiceOfferForm()
    return render(request, "offer_form.html", {"form": form})

@login_required
def exchanges(request):
    exchanges_list = (
        Exchange.objects.filter(Q(petitioner_id__user=request.user) | Q(offered_service__provider__user=request.user)).distinct().order_by("-agreed_date")
    )
    return render(request, "exchanges.html", {"exchanges": exchanges_list})

@login_required
def benefits(request):
    benefits_list = Benefit.objects.all()
    return render(request, "benefits.html", {"benefits": benefits_list})

@login_required
def request_exchange(request, offer_pk):
    offer = get_object_or_404(ServiceOffer, pk=offer_pk)
    petitioner_profile, _ = UserProfile.objects.get_or_create(user=request.user,
        defaults={
            "student_id": f"STU-{request.user.id}",
            "phone": "0000000000",
            "hours_balance": 4,
            "accumulated_hours": 0,
        },
    )
    if offer.provider == petitioner_profile or not offer.state_offer:
        return redirect("offer_detail", pk=offer.pk)

    if request.method == "POST":
        form = ExchangeRequestForm(
            request.POST,
            petitioner_profile=petitioner_profile,
            offer=offer,
        )
        if form.is_valid():
            exchange = form.save(commit=False)

            if (not exchange.offered_back and petitioner_profile.hours_balance < exchange.duration_hours):
                form.add_error("duration_hours", f"Insufficient balance. You currently have {petitioner_profile.hours_balance} hr(s) available.")
            else:
                exchange.exchange_id = f"EX-{uuid.uuid4().hex[:5].upper()}"
                exchange.petitioner_id = petitioner_profile
                exchange.offered_service = offer
                exchange.state_exchange = "PENDING"
                exchange.save()
                messages.success(
                    request, "Exchange request submitted successfully!"
                )
                return redirect("exchanges")
    else:
        form = ExchangeRequestForm(petitioner_profile=petitioner_profile, offer=offer)
    return render(request, "exchange_form.html", {"form": form, "offer": offer, "petitioner": petitioner_profile})