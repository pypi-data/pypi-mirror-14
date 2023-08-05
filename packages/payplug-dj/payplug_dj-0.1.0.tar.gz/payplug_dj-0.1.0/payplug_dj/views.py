# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, render

from .models import Payment
import payplug

from .signals import payment_return
from .signals import payment_cancel
from .signals import payment_notification


def PaymentAsk(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return redirect(payment.payplug_url)


def PaymentReturn(request, uuid):
    payment = get_object_or_404(Payment, uuid=uuid)
    payplug.set_secret_key(settings.PAYPLUG_API_KEY)
    payplug_payment = payplug.Payment.retrieve(payment.payplug_id)

    if payplug_payment.is_paid:  # and payplug_payment.is_live:
        payment.state = 'P'
        payment.save()
        payment_return.send(sender=payment.__class__, request=request, payment=payment)
        if payment.template_return == '':
            template_name = 'payplug_dj/payment_return.html'
        else:
            template_name = payment.template_return
            
        return render(
            request=request,
            template_name=template_name,
            context={
                'payment': payment,
                'payplug_payment': payplug_payment,
                'metadata': payment.get_payplug_metadata()
            }
        )
    else:
        payment_cancel.send(sender=payment.__class__, request=request, payment=payment)
        return PaymentCancel(request, uuid)


def PaymentCancel(request, uuid):
    payment = get_object_or_404(Payment, uuid=uuid)

    payplug.set_secret_key(settings.PAYPLUG_API_KEY)
    payplug_payment = payplug.Payment.retrieve(payment.payplug_id)

    payment.state = 'C'
    payment.save()

    if payment.template_cancel == '':
        template_name = 'payplug_dj/payment_cancel.html'
    else:
        template_name = payment.template_cancel

    payment_cancel.send(sender=payment.__class__, request=request, payment=payment)
    return render(
        request=request,
        template_name=template_name,
        context={
            'payment': payment,
            'payplug_payment': payplug_payment,
            'metadata': payment.get_payplug_metadata()
        }
    )


def PaymentNotification(request, uuid):
    """
    PaymentNotification : something arrived
    """
    # https://www.payplug.com/docs/api/guide.html?python#receive-a-notification-about-the-payment
    payment = get_object_or_404(Payment, uuid=uuid)

    payplug.set_secret_key(settings.PAYPLUG_API_KEY)
    payplug_payment = payplug.Payment.retrieve(payment.payplug_id)

    if payplug_payment.is_paid and payplug_payment.is_live:
        payment.state = 'P'
        payment.save()

    payment_notification.send(sender=payment.__class__, request=request, payment=payment)
    return render(
        request=request,
        template_name='payplug_dj/payment_notification.html',
        context={
            'payment': payment,
            'payplug_payment': payplug_payment,
            'metadata': payment.get_payplug_metadata()
        }
    )
