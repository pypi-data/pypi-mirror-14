// -*- coding: utf-8 -*-
// :Project:   hurm -- Login window
// :Created:   lun 01 feb 2016 20:34:00 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//

/*jsl:declare Ext*/

Ext.define('HuRM.window.Login', {
    extend: 'MP.window.Login',

    defaultFocus: 'email',

    getFormFields: function() {
        return [{
            xtype: 'container',
            height: 100,
            html: [
                '<img src="/static/images/logo.png"',
                '     style="margin-top: 15px; margin-left: 20px; float: left;">',
                '<div style="margin-top: 25px; text-align: center;">',
                '<b>HuRM</b><br/><br/>',
                _('Human Resources Manager'),
                '</div>'
            ].join('')
        }, {
            itemId: 'email',
            xtype: 'textfield',
            fieldLabel: _('Email'),
            name: 'email',
            vtype: 'email',
            allowBlank: false,
            anchor: '100%',
            selectOnFocus: true
        }, {
            xtype: 'textfield',
            fieldLabel: _('Password'),
            name: 'password',
            allowBlank: false,
            inputType: 'password',
            anchor: '100%',
            selectOnFocus: true
        }];
    }
});
