from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ServiceOffer, UserProfile

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
    class Meta:
        model = ServiceOffer
        fields = [
            "offer_id",
            "title",
            "description_offer",
            "provider",
            "category",
            "state_offer",
        ]
        labels = {
            "offer_id": "Offer ID",
            "title": "Service Title (max. 20 chars)",
            "description_offer": "Detailed Description",
            "provider": "Provider (Student)",
            "category": "Category",
            "state_offer": "Active Offer?",
        }
        widgets = {
            "offer_id": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., OF-005"}
            ),
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
            "provider": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "state_offer": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }