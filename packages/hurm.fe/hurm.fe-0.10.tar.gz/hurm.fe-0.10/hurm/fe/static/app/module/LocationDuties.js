// -*- coding: utf-8 -*-
// :Project:   hurm -- Location's duties
// :Created:   sab 13 feb 2016 20:15:04 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare HuRM*/
/*jsl:declare MP*/
/*jsl:declare _*/
/*jsl:declare ngettext*/

Ext.define('HuRM.module.LocationDuties', {
    extend: 'HuRM.module.Duties',

    id: 'location-duties-win',

    getFocusedConfig: function() {
        var me = this,
            edition = me.edition,
            location = me.focus;

        return {
            stickyFilters: [{
                id: 'edition',
                property: 'idedition',
                value: edition.get('idedition')
            }, {
                id: 'location',
                property: 'idlocation',
                value: location.get('idlocation')
            }]
        };
    },

    getFocusedTitle: function() {
        var me = this,
            edition = me.edition,
            location = me.focus;

        return Ext.String.format(
            // TRANSLATORS: this is the title of the location duties
            // window, params are location description and edition.
            _("Duties at location “{0}” in edition “{1}”"),
            location.get('description'), edition.get('description'));
    },

    getFocusedGridOverrides: function() {
        return {
            Location: {
                hidden: true
            }
        };
    },

    configureActionsForFocus: function(grid) {
        var aa = grid.findActionById('add');
        aa.hide();
    }
});
