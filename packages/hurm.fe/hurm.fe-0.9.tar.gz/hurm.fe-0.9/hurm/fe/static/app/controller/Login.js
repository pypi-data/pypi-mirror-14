// -*- coding: utf-8 -*-
// :Project:   hurm -- Login window controller
// :Created:   lun 01 feb 2016 20:30:28 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//

/*jsl:declare Ext*/

Ext.define('HuRM.desktop.App', {
    extend: 'MP.desktop.App',

    desktopConfig: {
        wallpaper: '/static/images/wallpapers/scrat.jpg',
        wallpaperStyle: 'stretch'
    },

    getStartConfig: function () {
        var config = this.callParent();

        config.height = 140;
        return config;
    }
});


Ext.define('HuRM.controller.Login', {
    extend: 'MP.controller.Login',

    applicationClass: 'HuRM.desktop.App'
});
