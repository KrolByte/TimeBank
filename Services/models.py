from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    PURPOSE_CHOICES = [
        ("SOCIAL_SERVICE", "Social service (scholarship)"),
        ("REWARDS", "Institutional rewards"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    student_id = models.CharField(max_length=10)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES, default="REWARDS")
    hours_balance = models.PositiveIntegerField(default=4)
    accumulated_hours = models.PositiveIntegerField()
    phone = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.username} ({self.hours_balance} hrs disponibles)"

class Category(models.Model):
    category_id = models.CharField(max_length=10)
    name_category = models.CharField(max_length=50)
    description_category = models.TextField()

    def __str__(self):
        return self.category_id

class Benefit(models.Model):
    BENEFIT_CHOICES = [
        ("SOCIAL_CERT", "Social service certificate (80 hrs)"),
        ("GRADE_50", "Academic incentive - Grade 5.0 (50 hrs)"),
        ("LUNCH", "Cafeteria dessert (80 hrs)"),
        ("COURSE", "Department in-person course slot (100 hrs)"),
    ]
    benefit_id = models.CharField(max_length=10)
    type_benefit = models.CharField(max_length=50, choices=BENEFIT_CHOICES)
    hours_used = models.IntegerField()
    application_date = models.DateField()
    delivery_state = models.BooleanField(default=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="benefits")

    def __str__(self):
        return self.benefit_id

class ServiceOffer(models.Model):
    offer_id = models.CharField(max_length=10)
    title = models.CharField(max_length=20)
    description_offer = models.TextField()
    state_offer = models.BooleanField(default=True)
    provider = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.offer_id

class Exchange(models.Model):
    STATE_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]
    QUALIFICATION_CHOICES = [
        (1, "1 - Very bad"),
        (2, "2 - Bad"),
        (3, "3 - Regular"),
        (4, "4 - Good"),
        (5, "5 - Excellent"),
    ]
    exchange_id = models.CharField(max_length=10)
    agreed_date = models.DateField()
    start_hour = models.TimeField()
    duration_hours = models.PositiveIntegerField(default=1)
    state_exchange = models.CharField(max_length=10, choices=STATE_CHOICES, default="PENDING")
    calification = models.IntegerField(choices=QUALIFICATION_CHOICES, null=True, blank=True)
    review = models.TextField()
    petitioner_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    offered_service = models.ForeignKey(ServiceOffer, on_delete=models.CASCADE, related_name="exchanges_requested",)
    offered_back = models.ForeignKey(ServiceOffer, on_delete=models.SET_NULL, null=True, blank=True, related_name="exchange_returned")

    def __str__(self):
        return self.exchange_id

class Schedule(models.Model):
    DAYS_CHOICES = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
        ("SAT", "Saturday"),
        ("SUN", "Sunday"),
    ]
    schedule_id = models.CharField(max_length=10)
    days_week = models.CharField(max_length=5, choices=DAYS_CHOICES)
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    offer = models.ForeignKey(ServiceOffer, on_delete=models.CASCADE)

    def __str__(self):
        return self.schedule_id