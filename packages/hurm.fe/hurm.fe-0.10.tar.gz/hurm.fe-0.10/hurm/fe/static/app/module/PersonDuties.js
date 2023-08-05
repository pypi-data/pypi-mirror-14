// -*- coding: utf-8 -*-
// :Project:   hurm -- Person's duties
// :Created:   sab 06 feb 2016 18:40:39 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare HuRM*/
/*jsl:declare MP*/
/*jsl:declare _*/
/*jsl:declare ngettext*/

Ext.define('HuRM.module.PersonDuties', {
    extend: 'HuRM.module.Duties',

    id: 'person-duties-win',

    getFocusedConfig: function() {
        var me = this,
            edition = me.edition,
            person = me.focus;

        return {
            stickyFilters: [{
                id: 'edition',
                property: 'idedition',
                value: edition.get('idedition')
            }, {
                id: 'person',
                property: 'idperson',
                value: person.get('idperson')
            }]
        };
    },

    getFocusedTitle: function() {
        var me = this,
            edition = me.edition,
            person = me.focus;

        return Ext.String.format(
            // TRANSLATORS: this is the title of the person duties
            // window, params are person name and edition.
            _("Duties assigned to {0} in edition “{1}”"),
            person.get('FullName'), edition.get('description'));
    },

    getFocusedGridOverrides: function() {
        return {
            Person: {
                hidden: true
            }
        };
    },

    configureActionsForFocus: function(grid) {
        var aa = grid.findActionById('add');
        aa.hide();
    }
});
