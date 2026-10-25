from django.contrib import admin
from .models import UserProfile, Category, Benefit, ServiceOffer,Exchange, Schedule

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Benefit)
admin.site.register(ServiceOffer)
admin.site.register(Exchange)
admin.site.register(Schedule)