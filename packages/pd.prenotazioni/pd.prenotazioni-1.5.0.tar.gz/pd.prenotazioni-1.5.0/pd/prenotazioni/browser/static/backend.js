/*globals jQuery, document */
/*jslint sloppy: true, vars: true, white: true, maxerr: 50, indent: 4 */
/*
 * This is the javascript to load tooltipster
 */
(function (document, jQuery) {
    function initTooltipster() {
        return jQuery('a.prenotazioni-popup').tooltipster({
            contentAsHTML: true,
            theme: 'tooltipster-light',
            functionBefore: function(origin, continueTooltip) {
                continueTooltip();
                if (origin.data('ajax') !== 'cached') {
                    jQuery.ajax({
                        type: 'POST',
                        url: origin.attr('href')+'/prenotazione_tooltip_view',
                        success: function(data) {
                            origin.tooltipster('content', data).data('ajax', 'cached');
                        }
                    });
                }
            }
        });
    }
    jQuery(document).ready(initTooltipster);
}(document, jQuery));
