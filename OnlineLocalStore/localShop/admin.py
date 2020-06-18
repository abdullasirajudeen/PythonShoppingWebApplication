from django.contrib import admin
from .models import userProfile, orderDetails, reviewDetails
# Register your models here.
admin.site.register(userProfile)
admin.site.register(orderDetails)
admin.site.register(reviewDetails)

