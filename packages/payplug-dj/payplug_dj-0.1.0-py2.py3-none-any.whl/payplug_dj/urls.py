# -*- coding: utf-8 -*-

from django.conf.urls import *
from .views import PaymentAsk
from .views import PaymentReturn, PaymentCancel, PaymentNotification

urlpatterns = [
    url(r'^ask/(?P<pk>[^/]+)$', PaymentAsk, name='ask'),
    url(r'^return/(?P<uuid>[^/]+)$', PaymentReturn, name='return'),
    url(r'^cancel/(?P<uuid>[^/]+)$', PaymentCancel, name='cancel'),
    url(r'^notification/(?P<uuid>[^/]+)$', PaymentNotification, name='notification'),
]

