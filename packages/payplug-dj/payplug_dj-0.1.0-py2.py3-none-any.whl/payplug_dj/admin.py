# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'email',
        'firstname',
        'lastname',
        'uuid',
        'amount',
        'currency',
        'payplug_id',
        'state',
    ]
    search_fields = ('payplug_id', 'firstname', 'lastname')

admin.site.register(Payment, PaymentAdmin)

