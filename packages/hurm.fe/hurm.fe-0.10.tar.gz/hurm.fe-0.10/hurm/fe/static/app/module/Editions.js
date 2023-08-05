// -*- coding: utf-8 -*-
// :Project:   hurm -- Editions management windows
// :Created:   mar 02 feb 2016 16:57:34 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare _*/
/*jsl:declare MP*/
/*jsl:declare HuRM*/

Ext.define('HuRM.module.Editions.Actions', {
    extend: 'MP.action.StoreAware',

    uses: [
        'Ext.Action',
        'Ext.form.field.TextArea',
        'MP.form.Panel',
        'MP.window.Notification'
    ],

    statics: {
        EDIT_ACTION: 'edit_edition',
        AVAILS_ACTION: 'avails',
        TASKS_ACTION: 'tasks',
        PRINT_DUTIES_BY_LOC_ACTION: 'print_duties_by_loc',
        PRINT_DUTIES_BY_PERSON_ACTION: 'print_duties_by_person',
        PRINT_PERSONS_DUTIES_SUMMARY_ACTION: 'print_persons_summary',
        DOWNLOAD_YAML_ACTION: 'download_yaml',
        DOWNLOAD_XLS_ACTION: 'download_xls'
    },

    initActions: function() {
        var me = this;
        var ids = me.statics();

        me.callParent();

        me.editAction = me.addAction(new Ext.Action({
            itemId: ids.EDIT_ACTION,
            text: _('Modify'),
            tooltip: _('Edit selected edition.'),
            iconCls: 'edit-record-icon',
            disabled: true,
            needsOneSelectedRow: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0];
                me.showEditWindow(record);
            }
        }));

        me.availsAction = me.addAction(new Ext.Action({
            itemId: ids.AVAILS_ACTION,
            text: _('Availabilities'),
            tooltip: _('Persons willing to cooperate to the selected edition.'),
            iconCls: 'persons-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    module = me.module.app.getModule('availabilities-win');
                module.createOrShowWindow(record);
            }
        }));

        me.tasksAction = me.addAction(new Ext.Action({
            itemId: ids.TASKS_ACTION,
            text: _('Tasks'),
            tooltip: _('Tasks related to the selected edition.'),
            iconCls: 'tasks-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    module = me.module.app.getModule('tasks-win');
                module.createOrShowWindow(record);
            }
        }));

        me.printDutiesByLocAction = me.addAction(new Ext.Action({
            itemId: ids.PRINT_DUTIES_BY_LOC_ACTION,
            text: _('Duties by location'),
            tooltip: _('Print all duties by location.'),
            iconCls: 'pdf-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    idedition = record.get('idedition'),
                    url = '/pdf/duties/edition/' + idedition + '/locations';
                window.open(url, "_blank");
            }
        }));

        me.printDutiesByPersonAction = me.addAction(new Ext.Action({
            itemId: ids.PRINT_DUTIES_BY_PERSON_ACTION,
            text: _('Duties by person'),
            tooltip: _('Print all duties by person.'),
            iconCls: 'pdf-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    idedition = record.get('idedition'),
                    url = '/pdf/duties/edition/' + idedition + '/persons';
                window.open(url, "_blank");
            }
        }));

        me.printPersonsDutiesSummaryAction = me.addAction(new Ext.Action({
            itemId: ids.PRINT_PERSONS_DUTIES_SUMMARY_ACTION,
            text: _('Persons duties summary'),
            tooltip: _('Print a summary of the duties of all involved persons.'),
            iconCls: 'pdf-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    idedition = record.get('idedition'),
                    url = '/pdf/duties/edition/' + idedition + '/summary';
                window.open(url, "_blank");
            }
        }));

        me.downloadYAMLAction = me.addAction(new Ext.Action({
            itemId: ids.DOWNLOAD_YAML_ACTION,
            text: _('Download as YAML'),
            tooltip: _('Get a YAML representation of the selected edition.'),
            iconCls: 'yaml-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    idedition = record.get('idedition'),
                    url = '/yaml/edition/' + idedition;
                window.open(url, "_blank");
            }
        }));

        me.downloadXLSAction = me.addAction(new Ext.Action({
            itemId: ids.DOWNLOAD_XLS_ACTION,
            text: _('Download as Excel'),
            tooltip: _('Get a Excel spreadsheet containing the selected edition.'),
            iconCls: 'excel-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    idedition = record.get('idedition'),
                    url = '/xls/edition/' + idedition;
                window.open(url, "_blank");
            }
        }));
    },

    attachActions: function() {
        var me = this;

        me.callParent();

        var tbar = me.component.child('#ttoolbar');

        tbar.add(2, ' ', me.editAction, me.availsAction, me.tasksAction, {
            text: _('Printouts'),
            iconCls: 'print-icon',
            menu: { items: [me.printDutiesByLocAction,
                            me.printDutiesByPersonAction,
                            me.printPersonsDutiesSummaryAction] }
        }, {
            text: _('Downloads'),
            iconCls: 'download-icon',
            menu: { items: [me.downloadYAMLAction,
                            me.downloadXLSAction]}
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
        var win = desktop.getWindow('edit-edition-win');

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        var metadata = me.module.config.metadata,
            size = desktop.getReasonableWindowSize(500, 310),
            editors = metadata.editors({
                '*': {
                    editor: MP.form.Panel.getDefaultEditorSettingsFunction('100%')
                },
                'note': {
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
                items: [editors.description,
                        editors.firstname,
                        editors.startdate,
                        editors.enddate,
                        editors.note],
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
            id: 'edit-edition-win',
            title: _('Edit edition'),
            iconCls: 'edit-edition-icon',
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


Ext.define('HuRM.module.Editions', {
    extend: 'MP.desktop.Module',

    requires: [
        'MP.grid.Panel'
    ],

    uses: [
        'HuRM.module.Editions.Actions'
    ],

    id: 'editions-win',
    iconCls: 'editions-icon',
    launcherText: _('Editions'),
    launcherTooltip: _('<b>Editions</b><br/>Editions management'),

    config: {
        xtype: 'editable-grid',
        pageSize: 23,
        autoShowAllEditors: false,
        clicksToEdit: 0,
        dataURL: '/data/editions',
        sorters: [{property: 'startdate', direction: 'DESC'}, 'enddate'],
        stripeRows: true
    },

    statics: {
        selectEdition: function(app, callback) {
            var form, model, store, win;

            model = Ext.define('MP.data.ImplicitModel-'+Ext.id(), {
                extend: 'Ext.data.Model',
                fields: ['idedition', 'description', 'startdate', 'enddate'],
                idProperty: 'idedition'
            });

            store = Ext.create('Ext.data.Store', {
                model: model,
                proxy: {
                    type: 'ajax',
                    url: '/data/editions?only_cols=idedition,description,startdate,enddate&sort=startdate&dir=DESC',
                    reader: {
                        type: 'json',
                        root: 'root',
                        idProperty: 'idedition',
                        totalProperty: 'count'
                    }
                }
            });

            form = new Ext.form.Panel({
                frame: true,
                bodyPadding: '10 10 0',
                defaults: {
                    labelWidth: 50,
                    anchor: '100%'
                },
                items: [{
                    xtype: 'combo',
                    store: store,
                    allowBlank: false,
                    autoSelect: true,
                    forceSelection: true,
                    displayField: 'description',
                    valueField: 'idedition',
                    listeners: {
                        afterrender: function(combo) {
                            store.load({
                                callback: function(records) {
                                    if(records.length)
                                        combo.select(records[0]);
                                }
                            });
                        }
                    }
                }],
                buttons: [{
                    text: _('Cancel'),
                    handler: function() {
                        win.destroy();
                    }
                }, {
                    text: _('Confirm'),
                    formBind: true,
                    handler: function() {
                        var frm = form.getForm();
                        if(frm.isValid()) {
                            var field = frm.getFields().items[0],
                                selrec = field.lastSelection.length && field.lastSelection[0];
                            if(selrec) {
                                win.destroy();
                                callback(selrec);
                            }
                        }
                    }
                }]
            });

            win = app.getDesktop().createWindow({
                title: _('Select edition'),
                width: 280,
                height: 110,
                layout: 'fit',
                minimizable: false,
                maximizable: false,
                items: [form]
            });

            win.show();
        }
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
                        Ext.create('HuRM.module.Editions.Actions', { module: me }),
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
                var size = desktop.getReasonableWindowSize(720, 300, "NW");

                win = desktop.createWindow({
                    id: me.id,
                    title: me.getLauncherText(),
                    x: size.x,
                    y: size.y,
                    width: size.width,
                    height: size.height,
                    iconCls: me.iconCls,
                    items: [me.config]
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
            }
        );
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
    }
});
