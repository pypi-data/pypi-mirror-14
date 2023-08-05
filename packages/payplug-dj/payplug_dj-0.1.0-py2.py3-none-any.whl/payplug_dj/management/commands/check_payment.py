# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
import payplug

from payplug_dj.models import Payment
from payplug_dj.signals import payment_return

class Command(BaseCommand):
    help = 'Check for payed but not cached by site'

    def handle(self, *args, **options):
        payplug.set_secret_key(settings.PAYPLUG_API_KEY)
        for payment in Payment.objects.exclude(state='P'):
            self.stdout.write('Checking Payment {}'.format(payment.pk))
            try:
                payplug_payment = payplug.Payment.retrieve(payment.payplug_id)
            except payplug.exceptions.NotFound:
                self.stdout.write('Payment not found {} / {}'.format(payment.pk, payment.payplug_id))
                continue

            if payplug_payment.is_paid and payment.state != 'P':
                payment.state = 'P'
                self.stdout.write('Payment {} has been paid'.format(payment.pk))
                payment.save()
                payment_return.send(sender=payment.__class__, request=None, payment=payment)

        return
