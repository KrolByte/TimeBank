from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Exchange, ServiceOffer, Category, Schedule, UserProfile

class StudentRegistrationForm(UserCreationForm):
    student_id = forms.CharField(
        max_length=10,
        label="Student ID",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g., 20241005"}
        ),
    )
    phone = forms.CharField(
        max_length=10,
        label="Phone Number",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "e.g., 3001234567"}
        ),
    )
    purpose = forms.ChoiceField(
        choices=UserProfile.PURPOSE_CHOICES,
        label="Platform Goal",
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
    # Crear categoría nueva si no existe en la lista
    new_category_name = forms.CharField(max_length=50, required=False, label="Or create a new category",
                                        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g., Graphic Design",
            }
        ),
    )
    new_category_description = forms.CharField(required=False, label="New category description",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Brief description of the new category",
            }
        ),
    )

    # Disponibilidad inicial (Schedule)
    days_week = forms.ChoiceField(
        choices=[("", "Select a day (optional)")] + Schedule.DAYS_CHOICES,
        required=False,
        label="Available Day",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    start_hour = forms.TimeField(
        required=False,
        label="Start Time",
        widget=forms.TimeInput(
            attrs={"class": "form-control", "type": "time"}
        ),
    )
    end_hour = forms.TimeField(
        required=False,
        label="End Time",
        widget=forms.TimeInput(
            attrs={"class": "form-control", "type": "time"}
        ),
    )
    class Meta:
        model = ServiceOffer
        fields = ["title", "description_offer", "category", "state_offer"]
        labels = {
            "title": "Service title (max. 20 chars)",
            "description_offer": "Detailed description",
            "category": "Category",
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
                    "placeholder": "Describe what you offer, topics, or requirements...",
                }
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "state_offer": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields["category"].required = False
    self.fields["category"].empty_label = ("Select a category or create a new one below")

def clean(self):
    cleaned_data = super().clean()
    category = cleaned_data.get("category")
    new_category_name = cleaned_data.get("new_category_name", "").strip()
    new_category_description = cleaned_data.get("new_category_description", "").strip()
    if not category and not new_category_name:
        raise forms.ValidationError(
            "Please select an existing category or provide a new category name."
        )
    if new_category_name and not new_category_description:
        raise forms.ValidationError(
            "Please provide a description for the new category."
        )
    day = cleaned_data.get("days_week")
    start = cleaned_data.get("start_hour")
    end = cleaned_data.get("end_hour")
    if any([day, start, end]) and not all([day, start, end]):
        raise forms.ValidationError(
            "If you provide availability, please fill in all fields: day, start time, and end time."
        )
    if start and end and start >= end:
        raise forms.ValidationError("End time must be after start time.")
    return cleaned_data

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = Exchange
        fields = [
            "agreed_date",
            "start_hour",
            "duration_hours",
            "offered_back",
            "review",
        ]
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

    def __init__(self, *args, petitioner_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["offered_back"].empty_label = (
            "None — Pay using my hours balance"
        )
        if petitioner_profile:
            self.fields["offered_back"].queryset = ServiceOffer.objects.filter(
                provider=petitioner_profile, state_offer=True
            )