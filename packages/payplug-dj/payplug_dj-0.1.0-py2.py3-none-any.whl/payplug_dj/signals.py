# -*- coding: utf-8 -*-

import django.dispatch
payment_return = django.dispatch.Signal(providing_args=["request", "payment"])
payment_cancel = django.dispatch.Signal(providing_args=["request", "payment"])
payment_notification = django.dispatch.Signal(providing_args=["request", "payment"])
