from django.contrib import admin
from .forms import ProfileForm
from .models import Profile, Payment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'balance')
    form = ProfileForm


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'value', 'created_at')
