// -*- coding: utf-8 -*-
// :Project:   hurm -- Frontend application entry point
// :Created:   lun 01 feb 2016 20:29:48 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//

/*jsl:declare Ext*/

Ext.Loader.setPath({
    MP: '/desktop/js'
});

Ext.application({
    name: 'HuRM',
    appFolder: '/static/app',
    controllers: [
        'Login'
    ],

    launch: function() {
        Ext.BLANK_IMAGE_URL = '/static/images/s.gif';
        Ext.create('HuRM.window.Login', {}).show();
    }
});
