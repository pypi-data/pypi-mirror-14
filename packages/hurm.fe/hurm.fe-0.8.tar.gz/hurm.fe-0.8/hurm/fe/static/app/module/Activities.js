// -*- coding: utf-8 -*-
// :Project:   hurm -- Activities management windows
// :Created:   mar 02 feb 2016 17:37:26 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare _*/
/*jsl:declare MP*/
/*jsl:declare HuRM*/

Ext.define('HuRM.module.Activities.Actions', {
    extend: 'MP.action.StoreAware',

    uses: [
        'Ext.Action',
        'Ext.form.field.TextArea',
        'MP.form.Panel',
        'MP.window.Notification'
    ],

    statics: {
        EDIT_ACTION: 'edit_activity',
        PAYLOADS_ACTION: 'activity_payloads'
    },

    initActions: function() {
        var me = this;
        var ids = me.statics();

        me.callParent();

        me.editAction = me.addAction(new Ext.Action({
            itemId: ids.EDIT_ACTION,
            text: _('Modify'),
            tooltip: _('Edit selected activity.'),
            iconCls: 'edit-record-icon',
            disabled: true,
            needsOneSelectedRow: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0];
                me.showEditWindow(record);
            }
        }));

        me.payloadsAction = me.addAction(new Ext.Action({
            itemId: ids.PAYLOADS_ACTION,
            text: _('Payloads'),
            tooltip: _('Modify associated payloads.'),
            iconCls: 'edit-record-icon',
            disabled: true,
            needsOneSelectedRow: true,
            needsCleanStore: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0],
                    module = me.module.app.getModule('activity-payloads-win');
                module.createOrShowWindow(record);
            }
        }));
    },

    attachActions: function() {
        var me = this;

        me.callParent();

        var tbar = me.component.child('#ttoolbar');

        tbar.add(2, ' ', me.editAction, me.payloadsAction);

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
        var win = desktop.getWindow('edit-activity-win');

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        var metadata = me.module.config.metadata,
            size = desktop.getReasonableWindowSize(500, 260),
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
                        editors.allowoverlappedduties,
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
            id: 'edit-activity-win',
            title: _('Edit activity'),
            iconCls: 'edit-activity-icon',
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


Ext.define('HuRM.module.Activities', {
    extend: 'MP.desktop.Module',

    requires: [
        'MP.grid.Panel'
    ],

    uses: [
        'HuRM.module.Activities.Actions'
    ],

    id: 'activities-win',
    iconCls: 'activities-icon',
    launcherText: _('Activities'),
    launcherTooltip: _('<b>Activities</b><br/>Activities management'),

    config: {
        xtype: 'editable-grid',
        pageSize: 23,
        autoShowAllEditors: false,
        clicksToEdit: 0,
        dataURL: '/data/activities',
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
                        Ext.create('HuRM.module.Activities.Actions', { module: me }),
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
                var size = desktop.getReasonableWindowSize(570, 250);

                win = desktop.createWindow({
                    id: me.id,
                    title: me.getLauncherText(),
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
    }
});
