
1.5.0 (2016-03-16)
------------------

New:

- The logo for the pdf is now configurable through zope.conf
  [ale-rt]

1.4.0 (2016-03-15)
------------------

- Try to support all versions of collective.fontawesome
  [ale-rt, pnicolli]
- Improved logo quality in pdf printout
  [ale-rt, pnicolli]


1.3.1 (2015-08-10)
------------------

- Properly set encoding to utf8 when registering pdf view
  [ale-rt]


1.3.0 (2014-11-06)
------------------

- user_can_search method moved to prenotazioni_context_state.


1.2.3 (2014-09-15)
------------------

- Fix csv encoding.
- Modified content_rules patch
  [ale-rt]


1.2.2 (2014-09-12)
------------------

- When deciding the required fields in prenotazione_add form don't touch
  some fields
  [ale-rt]


1.2.1 (2014-09-11)
------------------

- Look for permission in context_state view
  [alert]


1.2.0 (2014-09-10)
------------------

- Requires rg.prenotazioni >= 3.5.0
- Adds with an extender the capability to make reservation for the same day
- Adds with an extender the capability to specify the fields required
  at booking time
- Handling statistics
  [alert]

1.1.1 (2014-06-23)
------------------

- Fix encoding problem.


1.1.0 (unreleased)
------------------

- Index also revision history
- Added Tooltipster
  [alert]


1.0.1 (2014-06-04)
------------------

- Patch per gestione di contentrules
- Modified search results for prenotazioni
- Small modifications on pdf
- Added a confirmation page for anonymous users.
- Readers can search bookings
- Requires rg.prenotazioni > 3.3.0.dev0
  [alert]


1.0.0 (2014-05-05)
------------------

- Upgrade step for repositorytool profile [nicolasenno]
- Added to logger detail about modification, old value new value [nicolasenno]·
- Added logger for IPrenotazione objects modification [nicolasenno]
- Patching Prenotazione schema to allow modification to prenotazione objects
  without email [alert]
- Removed buttons from the folder_contents view of PrenotazioniFolder [alert]
- Removed actions menu for Prenotazione [alert]
- Aggiunto validatore campi email, telefono e cellulare in form richiesta
  prenotazioni [nicolasenno]
- Added events logger for IPrenotazione [nicolasenno]
- Rimosso campo email obbligatorio form richiesta prenotazioni [nicolasenno]
- Added event handler logger
- Package created using templer
  [RedTurtle Technology]
