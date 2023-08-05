# -*- coding: utf-8 -*-

from django.db import models
import uuid

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

import payplug


PAYMENT_STATE = (
    ('C', 'Canceled'),
    ('P', 'Paid'),
    ('R', 'Refund'),
    ('W', 'Wait for payment'),
    )


class Payment(models.Model):
    """
    Payment interface with Payplug
    """

    email = models.CharField(
        _('email'),
        max_length=50,
        )
    firstname = models.CharField(
        _('Firstname'),
        max_length=50,
        )
    lastname = models.CharField(
        _('Lastname'),
        max_length=50,
        )

    uuid = models.UUIDField(
        _('UUID for transactions'),
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    amount = models.FloatField(
        _('Amount'),
        default=0,
    )
    currency = models.CharField(
        _('Currency'),
        max_length=10,
        default='EUR',
    )

    payplug_id = models.CharField(
        _('PayPlug transaction ID'),
        max_length=150,
        default='',
        blank=True,
        null=True,
    )

    payplug_url = models.CharField(
        _('PayPlug transaction URL'),
        max_length=150,
        default='',
        blank=True,
        null=True,
    )

    state = models.CharField(
        _('Payment state'),
        choices=PAYMENT_STATE,
        max_length=1,
        default='W',
    )

    template_return = models.CharField(
        _('Return template name'),
        max_length=150,
        default='',
        blank=True,
        null=True,
    )
    template_cancel = models.CharField(
        _('Cancel template name'),
        max_length=150,
        default='',
        blank=True,
        null=True,
    )

    def get_payplug_metadata(self):
        payplug.set_secret_key(settings.PAYPLUG_API_KEY)
        payplug_payment = payplug.Payment.retrieve(self.payplug_id)
        try:
            return payplug_payment.metadata
        except AttributeError:
            return None

    def create_payment(self, metadata={}):
        payplug.set_secret_key(settings.PAYPLUG_API_KEY)
        # base_url = ''
        payment_data = {
            'amount': int(self.amount * 100),
            'currency': self.currency,
            'customer': {
                'email': self.email,
                'first_name': self.firstname,
                'last_name': self.lastname,
            },
            'hosted_payment': {
                'return_url': ''.join([
                    'http://',
                    Site.objects.get_current().domain,
                    reverse(
                        'payplug_dj:return',
                        kwargs={'uuid': str(self.uuid)}
                    )]),
                'cancel_url': ''.join([
                    'http://',
                     Site.objects.get_current().domain,
                    reverse(
                        'payplug_dj:cancel',
                        kwargs={'uuid': str(self.uuid)}
                    )]),
            },
            'notification_url': ''.join([
                'http://',
                Site.objects.get_current().domain,
                reverse(
                    'payplug_dj:notification',
                    kwargs={'uuid': str(self.uuid)}
                )]),
            'metadata': metadata,
        }

        payplug_payment = payplug.Payment.create(**payment_data)

        self.payplug_id = payplug_payment.id
        self.payplug_url = payplug_payment.hosted_payment.payment_url
        self.save()
        return
