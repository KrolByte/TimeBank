from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user_id = models.CharField(max_length=10)
    purpose = models.CharField(max_length=20)
    hours_balance = models.PositiveIntegerField()
    accumulated_hours = models.PositiveIntegerField()
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.user_id

class Category(models.Model):
    category_id = models.CharField(max_length=10)
    name_category = models.CharField(max_length=50)
    description_category = models.TextField()

    def __str__(self):
        return self.category_id

class Benefit(models.Model):
    benefit_id = models.CharField(max_length=10)
    type_benefit = models.CharField(max_length=50)
    hours_used = models.TimeField()
    application_date = models.DateField()
    delivery_state = models.CharField(max_length=10)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.benefit_id

class ServiceOffer(models.Model):
    offer_id = models.CharField(max_length=10)
    title = models.CharField(max_length=20)
    description_offer = models.TextField()
    state_offer = models.BooleanField()
    provider_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.offer_id

class Exchange(models.Model):
    exchange_id = models.CharField(max_length=10)
    agreed_date = models.DateField()
    start_hour = models.TimeField()
    duration_hours = models.PositiveIntegerField()
    state_exchange = models.CharField(max_length=10)
    calification = models.PositiveSmallIntegerField()
    review = models.TextField()
    petitioner_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    offer_id = models.ForeignKey(ServiceOffer, on_delete=models.CASCADE)

    def __str__(self):
        return self.exchange_id

class Schedule(models.Model):
    schedule_id = models.CharField(max_length=10)
    days_week = models.CharField(max_length=10)
    start_hour = models.TimeField()
    deadline = models.TimeField()
    offer_id = models.ForeignKey(ServiceOffer, on_delete=models.CASCADE)

    def __str__(self):
        return self.schedule_id