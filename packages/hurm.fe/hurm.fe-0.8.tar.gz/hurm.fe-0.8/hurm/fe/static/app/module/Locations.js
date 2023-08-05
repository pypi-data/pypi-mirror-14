// -*- coding: utf-8 -*-
// :Project:   hurm -- Locations management windows
// :Created:   mar 02 feb 2016 18:53:16 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//


/*jsl:declare Ext*/
/*jsl:declare _*/
/*jsl:declare MP*/
/*jsl:declare HuRM*/

Ext.define('HuRM.module.Locations.Actions', {
    extend: 'MP.action.StoreAware',

    uses: [
        'Ext.Action',
        'Ext.form.field.TextArea',
        'MP.form.Panel',
        'MP.window.Notification'
    ],

    statics: {
        EDIT_ACTION: 'edit_location',
        TASKS_ACTION: 'tasks',
        DUTIES_ACTION: 'location_duties',
        PRINT_DUTIES_ACTION: 'print_duties'
    },

    initActions: function() {
        var me = this;
        var ids = me.statics();

        me.callParent();

        me.editAction = me.addAction(new Ext.Action({
            itemId: ids.EDIT_ACTION,
            text: _('Modify'),
            tooltip: _('Edit selected location.'),
            iconCls: 'edit-record-icon',
            disabled: true,
            needsOneSelectedRow: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0];
                me.showEditWindow(record);
            }
        }));

        me.tasksAction = me.addAction(new Ext.Action({
            itemId: ids.TASKS_ACTION,
            text: _('Tasks'),
            tooltip: _('Tasks related to the selected location.'),
            iconCls: 'tasks-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0];
                me.module.showTasksWindow(record);
            }
        }));

        me.dutiesAction = me.addAction(new Ext.Action({
            itemId: ids.DUTIES_ACTION,
            text: _('Duties'),
            tooltip: _('Duties related to the selected location.'),
            iconCls: 'duties-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0];
                me.module.showDutiesWindow(record);
            }
        }));

        me.printDutiesAction = me.addAction(new Ext.Action({
            itemId: ids.PRINT_DUTIES_ACTION,
            text: _('Duties'),
            tooltip: _('Print this location duties.'),
            iconCls: 'pdf-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0];
                me.module.printDuties(record);
            }
        }));
    },

    attachActions: function() {
        var me = this;

        me.callParent();

        var tbar = me.component.child('#ttoolbar');

        tbar.add(2, ' ', me.editAction, me.tasksAction, me.dutiesAction, {
            text: _('Printouts'),
            iconCls: 'print-icon',
            menu: { items: [me.printDutiesAction] }
        });

        me.component.on({
            itemdblclick: function() {
                if(!me.editAction.isDisabled())
                    me.editAction.execute();
            }
        });

        me.component.store.on({
            add: function(store, records) {
                //jsl:unused store
                var record = records[0];
                me.showEditWindow(record);
            }
        });
    },

    showEditWindow: function(record) {
        var me = this;
        var desktop = me.module.app.getDesktop();
        var win = desktop.getWindow('edit-location-win');

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        var metadata = me.module.config.metadata,
            size = desktop.getReasonableWindowSize(800, 410),
            orig_url,
            editors = metadata.editors({
                '*': {
                    editor: MP.form.Panel.getDefaultEditorSettingsFunction('100%')
                },
                Province: {
                    editor: {
                        listeners: {
                            beforequery: function(event) {
                                var store = event.combo.store,
                                    countryf = form.getForm().findField(editors.Country.name),
                                    country;
                                if(!Ext.isEmpty(countryf.lastSelection)) {
                                    var iname = countryf.store.proxy.reader.idProperty,
                                    srec = countryf.lastSelection[0];
                                    country = srec.get(iname);
                                } else {
                                    country = record.get('country');
                                }
                                if(!orig_url) {
                                    orig_url = store.proxy.url;
                                }
                                store.proxy.url = Ext.String.urlAppend(orig_url,
                                                                       'country='+country);
                                delete event.combo.lastQuery;
                            }
                        }
                    }
                },
                note: {
                    editor: {
                        xtype: 'textarea'
                    }
                }
            }),
            form = Ext.create('MP.form.Panel', {
                autoScroll: true,
                fieldDefaults: {
                    labelWidth: 100,
                    margin: '15 10 0 10'
                },
                items: [{
                    xtype: 'container',
                    layout: 'hbox',
                    items: [{
                        xtype: 'container',
                        layout: 'anchor',
                        flex: 1,
                        items: [
                            editors.description,
                            editors.phone,
                            editors.mobile,
                            editors.email
                        ]
                    }, {
                        xtype: 'container',
                        layout: 'anchor',
                        flex: 1,
                        items: [
                            editors.Country,
                            editors.Province,
                            editors.zip,
                            editors.city,
                            editors.address
                        ]
                    }]
                }, editors.note
                       ],
                buttons: [{
                    text: _('Cancel'),
                    handler: function() {
                        if(record.phantom) {
                            record.store.deleteRecord(record);
                        }
                        win.close();
                    }
                }, {
                    text: _('Confirm'),
                    formBind: true,
                    handler: function() {
                        if(form.isValid()) {
                            form.updateRecord(record);
                            win.close();
                            Ext.create("MP.window.Notification", {
                                position: 't',
                                width: 260,
                                title: _('Changes have been applied…'),
                                html: _('Your changes have been applied <strong>locally</strong>.<br/><br/>To make them permanent you must click on the <blink>Save</blink> button.'),
                                iconCls: 'info-icon'
                            }).show();
                        }
                    }
                }]
            });

        win = desktop.createWindow({
            id: 'edit-location-win',
            title: _('Edit location'),
            iconCls: 'edit-location-icon',
            width: size.width,
            height: size.height,
            modal: true,
            items: form,
            closable: false,
            minimizable: false,
            maximizable: false,
            resizable: false
        });

        form.loadRecord(record);

        win.show();
    }
});


Ext.define('HuRM.module.Locations', {
    extend: 'MP.desktop.Module',

    requires: [
        'MP.grid.Panel'
    ],

    uses: [
        'HuRM.module.Locations.Actions'
    ],

    id: 'locations-win',
    iconCls: 'locations-icon',
    launcherText: _('Locations'),
    launcherTooltip: _('<b>Locations</b><br/>Locations management'),

    config: {
        xtype: 'editable-grid',
        pageSize: 23,
        autoShowAllEditors: false,
        clicksToEdit: 0,
        dataURL: '/data/locations',
        sorters: ['description'],
        stripeRows: true
    },

    getConfig: function(callback) {
        var me = this,
            config = me.config;

        if(!config.metadata) {
            MP.data.MetaData.fetch(config.dataURL, me, function(metadata) {
                var overrides = {},
                    fields = metadata.fields(overrides);

                Ext.apply(config, {
                    metadata: metadata,
                    fields: fields,
                    columns: metadata.columns(overrides, false),
                    idProperty: metadata.primary_key,
                    totalProperty: metadata.count_slot,
                    successProperty: metadata.success_slot,
                    rootProperty: metadata.root_slot,
                    plugins: [
                        Ext.create('HuRM.module.Locations.Actions', { module: me }),
                    ]
                });
                callback(config);
                me.app.on('logout', function() { delete config.metadata; }, me, { single: true });
            });
        } else {
            callback(config);
        }
    },

    createOrShowWindow: function() {
        var me = this,
            desktop = me.app.getDesktop(),
            win = desktop.getWindow(me.id);

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        me.configure(
            [me.getConfig],
            function(done) {
                var size = desktop.getReasonableWindowSize(800, 640, "NE"),
                    config = Ext.apply({
                        newRecordData: {
                            country: 'IT',
                            Country: _("Italy"),
                            province: 'IT-TN',
                            Province: _("Trento")
                        }
                    }, me.config);

                win = desktop.createWindow({
                    id: me.id,
                    title: me.getLauncherText(),
                    x: size.x,
                    y: size.y,
                    width: size.width,
                    height: size.height,
                    iconCls: me.iconCls,
                    items: [config]
                });

                var grid = win.child('editable-grid');

                // Fetch the first page of records, and when done show
                // the window
                grid.store.load({
                    params: {start: 0, limit: me.pageSize},
                    callback: function() {
                        win.on({show: done, single: true});
                        win.show();
                    }
                });

                var da = grid.findActionById('delete');
                da.shouldBeDisabled = me.shouldDisableDeleteAction.bind(grid);
            });
    },

    shouldDisableDeleteAction: function() {
        var grid = this;
        var sm = grid.getSelectionModel();

        if(sm.getCount() > 0) {
            var selrecs = sm.getSelection();
            var disable = false;

            for(var i=selrecs.length-1; i>=0; i--) {
                var record = selrecs[i];

                if(record.get('Tasks') > 0) {
                    disable = true;
                    break;
                }
            }
            return disable;
        } else {
            return true;
        }
    },

    showTasksWindow: function(location) {
        var me = this;

        HuRM.module.Editions.selectEdition(me.app, function(edition) {
            me.app.getModule('tasks-win')
                .createOrShowWindow(edition, location);
        });
    },

    showDutiesWindow: function(location) {
        var me = this;

        HuRM.module.Editions.selectEdition(me.app, function(edition) {
            me.app.getModule('location-duties-win')
                .createOrShowWindow(edition, location);
        });
    },

    printDuties: function(location) {
        var me = this;

        HuRM.module.Editions.selectEdition(me.app, function(edition) {
            var url = '/pdf/duties/edition/'
                + edition.get('idedition')
                + '/location/' + location.get('idlocation');
            window.open(url, "_blank");
        });
    }
});
