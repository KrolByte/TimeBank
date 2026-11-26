from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Exchange, ServiceOffer, Category, Schedule, UserProfile
from datetime import datetime, timedelta

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Institutional or Personal Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "student@example.com"}
        ),
    )
    student_id = forms.CharField(max_length=10, label="Student ID",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "ex., 20241005"}
        ),
    )
    phone = forms.CharField(max_length=10, label="Phone Number",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "ex., 3001234567"}
        ),
    )
    purpose = forms.ChoiceField(choices=UserProfile.PURPOSE_CHOICES, label="Platform Goal",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})

class ServiceOfferForm(forms.ModelForm):
    # Declarado fuera de Meta.fields para que el modelo no exija este campo antes de guardar
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Existing Category",
        empty_label="-- Select an existing category --",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    # Campos para nueva categoría
    new_category_name = forms.CharField(
        max_length=50,
        required=False,
        label="New Category Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g., Graphic Design",
            }
        ),
    )
    new_category_description = forms.CharField(
        required=False,
        label="New Category Description",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Brief description of the new category",
            }
        ),
    )
    # Campos de disponibilidad obligatorios (Schedule)
    days_week = forms.ChoiceField(
        choices=[("", "-- Select a day --")] + Schedule.DAYS_CHOICES,
        required=True,
        label="Available Day",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    start_hour = forms.TimeField(
        required=True,
        label="Start Time",
        widget=forms.TimeInput(
            attrs={"class": "form-control", "type": "time"}
        ),
    )
    end_hour = forms.TimeField(
        required=True,
        label="End Time",
        widget=forms.TimeInput(
            attrs={"class": "form-control", "type": "time"}
        ),
    )

    class Meta:
        model = ServiceOffer
        # Quitamos "category" de aquí; lo asignamos manualmente en views.py
        fields = ["title", "description_offer", "state_offer"]
        labels = {
            "title": "Service Title (max. 20 chars)",
            "description_offer": "Detailed Description",
            "state_offer": "Active Offer?",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Calculus Tutoring",
                }
            ),
            "description_offer": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Describe what you will teach or help with...",
                }
            ),
            "state_offer": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        new_cat_name = cleaned_data.get("new_category_name", "").strip()
        new_cat_desc = cleaned_data.get("new_category_description", "").strip()
        if category and new_cat_name:
            raise forms.ValidationError(
                "Please either select an existing category OR create a new one, not both."
            )
        if not category and not new_cat_name:
            raise forms.ValidationError(
                "You must select an existing category or add a new category."
            )
        if new_cat_name and not new_cat_desc:
            self.add_error(
                "new_category_description",
                "Description is required when adding a new category.",
            )
        start = cleaned_data.get("start_hour")
        end = cleaned_data.get("end_hour")
        if start and end and start >= end:
            self.add_error("end_hour", "End time must be after start time.")
        return cleaned_data

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = ["agreed_date", "start_hour", "duration_hours", "offered_back", "review"]
        labels = {
            "agreed_date": "Preferred date",
            "start_hour": "Start time",
            "duration_hours": "Duration (Hours)",
            "offered_back": "Offer a service in return (Optional — Barter)",
            "review": "Message or notes for the Provider",
        }
        widgets = {
            "agreed_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "start_hour": forms.TimeInput(
                attrs={"class": "form-control", "type": "time"}
            ),
            "duration_hours": forms.NumberInput(
                attrs={"class": "form-control", "min": "1", "max": "4"}
            ),
            "offered_back": forms.Select(attrs={"class": "form-select"}),
            "review": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Share details about what you need help with...",
                }
            ),
        }

    def __init__(self, *args, petitioner_profile=None, offer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.offer = offer
        self.fields["offered_back"].empty_label = (
            "None — Pay using my hours balance"
        )
        if petitioner_profile:
            self.fields["offered_back"].queryset = ServiceOffer.objects.filter(
                provider=petitioner_profile, state_offer=True
            )

    #Validación del rango horario del proveedor
    def clean(self):
        cleaned_data = super().clean()
        agreed_date = cleaned_data.get("agreed_date")
        start_hour = cleaned_data.get("start_hour")
        duration_hours = cleaned_data.get("duration_hours")

        if not (agreed_date and start_hour and duration_hours and self.offer):
            return cleaned_data

        # Validar que la fecha no sea en el pasado
        if agreed_date < datetime.now().date():
            self.add_error("agreed_date", "You cannot select a past date.")
            return cleaned_data

        # Verificar disponibilidad del proveedor si tiene horarios registrados
        schedules = self.offer.schedule_set.all()
        if schedules.exists():
            # Mapear número de día de la semana (0=Lunes ... 6=Domingo) a los códigos habituales
            weekday_num = agreed_date.weekday()
            day_aliases = {
                0: ["MON", "LUN", "MONDAY", "LUNES", "0", "1"],
                1: ["TUE", "MAR", "TUESDAY", "MARTES", "1", "2"],
                2: ["WED", "MIE", "MIÉ", "WEDNESDAY", "MIERCOLES", "MIÉRCOLES", "2", "3"],
                3: ["THU", "JUE", "THURSDAY", "JUEVES", "3", "4"],
                4: ["FRI", "VIE", "FRIDAY", "VIERNES", "4", "5"],
                5: ["SAT", "SAB", "SÁB", "SATURDAY", "SABADO", "SÁBADO", "5", "6"],
                6: ["SUN", "DOM", "SUNDAY", "DOMINGO", "6", "7"],
            }
            valid_codes = day_aliases[weekday_num]

            matching_schedules = [
                s
                for s in schedules
                if str(s.days_week).strip().upper() in valid_codes
            ]

            if not matching_schedules:
                available_days = ", ".join(
                    s.get_days_week_display() for s in schedules
                )
                self.add_error(
                    "agreed_date",
                    f"The provider is only available on: {available_days}.",
                )
                return cleaned_data

            # Calcular hora de finalización solicitada
            start_dt = datetime.combine(agreed_date, start_hour)
            end_dt = start_dt + timedelta(hours=duration_hours)

            # Verificar si cabe dentro de alguna franja horaria de ese día
            fits_schedule = False
            for s in matching_schedules:
                sched_start = datetime.combine(agreed_date, s.start_hour)
                sched_end = datetime.combine(agreed_date, s.end_hour)
                if start_dt >= sched_start and end_dt <= sched_end:
                    fits_schedule = True
                    break

            if not fits_schedule:
                ranges = ", ".join(
                    f"{s.start_hour.strftime('%I:%M %p')} - {s.end_hour.strftime('%I:%M %p')}"
                    for s in matching_schedules
                )
                self.add_error(
                    "start_hour",
                    f"Requested time + duration exceeds the provider's schedule ({ranges}).",
                )

        return cleaned_data