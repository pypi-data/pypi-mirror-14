# -*- coding: utf-8 -*-
from App.config import getConfiguration
from pd.prenotazioni import prenotazioniMessageFactory as _
from plone.memoize.view import memoize
from rg.prenotazioni.browser.prenotazione_print import PrenotazionePrint


class PrenotazionePrintPDF(PrenotazionePrint):
    '''
    This is a view to proxy autorizzazione
    '''
    title = _("booking_receipt", "Booking receipt")

    footer_text = "Comune di Padova - Sistema di prenotazione unico"

    @property
    @memoize
    def logo_path(self):
        ''' get the logo path from the configuration
        '''
        product_config = getattr(getConfiguration(), 'product_config', {})
        config = product_config.get('pd.prenotazioni', {})
        logo = config.get('logo', '')
        return logo

    @property
    @memoize
    def rml_options(self):
        '''
        Return the options for this prenotazione
        '''
        return {
            'prenotazione': self.prenotazione,
            'logo': self.logo_path
        }
