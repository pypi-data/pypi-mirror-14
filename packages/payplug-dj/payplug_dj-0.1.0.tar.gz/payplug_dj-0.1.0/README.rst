=============================
payplug-dj
=============================

A Django module for using https://www.payplug.com payment solution.

Documentation
-------------

The full documentation is at https://payplug_dj.readthedocs.org.

Quickstart
----------

Install payplug-dj::

    pip install payplug_dj

Then use it in a project, add::

  'payplug_dj'

to your ``INSTALLED_APPS`` and set your PAYPLUG_API_KEY in your ``settings.py``::

   PAYPLUG_API_KEY = 'sk_test_XXXXxxxXXXX'

To use it in your application views:: 
   
    from payplug_dj.models import Payment
    from payplug_dj.signals import payment_return
    from payplug_dj.signals import payment_cancel
    
    payment = Payment.objects.create(
        email='mail@example.com,
        firstname='Alexandre',
        lastname='Norman',
        amount=12.45,
        currency='EUR',
        template_return='myapp/payment_return.html',
        template_cancel='myapp/payment_cancel.html',
    )
    payment.save()
    payment.create_payment(
        metadata={
            'my_invoice_id': '2016-0002',
            'my_client_id': 142,
        }
    )
    
    payment_return.connect(PaymentOk)
    payment_return.connect(PaymentCancelled)
    
    
    def PaymentOk(sender, **kwargs):
        request = kwargs.get("request")
        payment = kwargs.get("payment")
        metadata = payment.get_payplug_metadata()
    
        # Set payment OK
        if payment.state == 'P':
            # Do something
            pass
        return
    
    def PaymentCancelled(sender, **kwargs):
        # Do something
        return


``payment.state`` could take one of this values:

* 'C': Canceled
* 'P': Paid
* 'R': Refund
* 'W': Wait for payment

        
        
Features
--------

* Allow to use Payplug payment solution from Django.

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  cookiecutter-djangopackage_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _cookiecutter-djangopackage: https://github.com/pydanny/cookiecutter-djangopackage
