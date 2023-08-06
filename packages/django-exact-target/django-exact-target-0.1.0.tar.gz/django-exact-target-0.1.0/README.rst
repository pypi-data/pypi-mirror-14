===================
django-exact-target
===================

This library serves as a connector between `django` and the `Exact Target REST API <https://code.exacttarget.com/apis-sdks/rest-api/v1/routes.html>`_.

Installation
============

Install using pip.::

    $ pip install django-exact-target

Add your exact target client settings to your Django project's settings.py file.::

    EXACT_TARGET_CLIENT_ID = 'my-client-id...'
    EXACT_TARGET_CLIENT_SECRET = 'my-client-secret...'

Usage
=====

Dispatch a `TriggeredSend`. See also `message definition sends <https://code.exacttarget.com/apis-sdks/rest-api/v1/messaging/messageDefinitionSends.html>`_.::

    from exacttarget.messages import TriggeredSend

    sender = TriggeredSend('my-triggered-send-id')
    sender.dispatch('foo@example.com', {
        # SubscriberAttributes
        "Region": "West",
        "City": "Indianapolis",
        "State": "IN"
    })


Changelog
=========

0.1.0
------------------
- Initial release.
