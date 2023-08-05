.. contents::

Introduction
============

A **booking product for Plone** to reserve time slots throughout the week.


Customizations
==============

This product is an extension that customizes `rg.prenotazioni`__

__ https://pypi.python.org/pypi/rg.prenotazioni


Booking folder content type
---------------------------

This package provides an extender to add the fields:

1. required_booking_fields
2. same_day_booking_disallowed

The field "required_booking_fields" allows to specify which of the fields:

- email
- mobile
- phone
- subject
- agency

should be mandatory for a booking request to be accepted.
In any case at least one between email, mobile and phone
should be given at booking time.

The field "same_day_booking_disallowed" has 3 possible states:
    
1. Yes
2. No
3. No, just for today

If 1. is selected the default behavior of
`rg.prenotazioni`__
is maintained: users cannot reserve a booking today.

__ https://pypi.python.org/pypi/rg.prenotazioni

Options 2. and 3. instead allow the reservation.

prenotazioni_context_state
--------------------------

Extends the `rg.prenotazioni homonymous view`__ in order to override the
minimum date since when it is possible to reserve a booking.

__ https://github.com/PloneGov-IT/rg.prenotazioni/blob/master/rg/prenotazioni/browser/prenotazioni_context_state.py#L59

Extends the `rg.prenotazioni homonymous view`__ in order to override
the attribute ``add_view``.
If a parameter called ``form.add_view`` is passed, it will be used
as the add form for a booking object.

We use this in combination with an apache rewrite rule that injects in the
request the parameter with the value ``prenotazioni_add_ro``::

    RewriteCond %{QUERY_STRING} !((.*)form_add_view=(.*))
    RewriteRule ^/path_to_enable_custom_form/(.*) /notheme/$1?form.add_view=prenotazione_add_ro [QSA]

__ https://github.com/PloneGov-IT/rg.prenotazioni/blob/master/rg/prenotazioni/browser/prenotazioni_context_state.py#L59


Custom mail action
------------------

The product overrides the mail action defined by
`collective.contentrules.mailfromfield`__, providing additional markers
dedicate to the booking product:

- `${gate}`
- `${date}`
- `${time}`
- `${type}`

__ https://pypi.python.org/pypi/collective.contentrules.mailfromfield


Custom event log
----------------

The product registers, optionally, some events to an external logfile:

- booking creation
- booking workflow state modification
- booking date/time modification

In order to track modification the product adds the booking content type
to the reposository tool.

The custom event log has to be enabled adding to the instance part
of your buildout this snippet::

  zope-conf-additional +=
    <product-config pd.prenotazioni>
        logfile ${buildout:directory}/var/log/prenotazioni.log
    </product-config>

Event log views
---------------

The logged events can also be viewed online
using thew ``booking_stats`` form.

The form displays to the user the data of the agendas he can manage
contained under the context path.

Calling this view on the root of the Plone site return data from all
the manageable agendas.

The view displays data in a table and provides a link and an action
for downloading the logged events in a csv file.

There is also a view, called ``booking_stats_delete``,
that will delete all the log entry inserted before
the specified date.


Customized Searchable text
--------------------------

Searchable text for booking objects is customized in order to add
the modification comments to the index.

The product removes from the booking searchable text those fields:

- gate
- subject
- location


Popup with tooltipster
----------------------

The product adds to the agenda some pop-ups using the library `tooltipster`__

__ http://iamceege.github.io/tooltipster/


Credits
=======

Developed with the support of `Comune di Padova`__;
Comune di Padova supports the `PloneGov initiative`__.

.. image:: https://raw.githubusercontent.com/PloneGov-IT/pd.prenotazioni/master/docs/logo-comune-pd-150x200.jpg
   :alt: Comune di Padova's logo

__ http://www.padovanet.it/
__ http://www.plonegov.it/


Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
      :target: http://www.redturtle.it/


