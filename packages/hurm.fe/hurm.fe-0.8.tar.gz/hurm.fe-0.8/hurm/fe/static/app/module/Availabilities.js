// -*- coding: utf-8 -*-
// :Project:   hurm -- Availabilities management windows
// :Created:   mar 02 feb 2016 23:30:32 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare _*/
/*jsl:declare MP*/
/*jsl:declare HuRM*/

Ext.define('HuRM.module.Availabilities.Actions', {
    extend: 'MP.action.StoreAware',

    uses: [
        'Ext.Action',
        'Ext.form.field.TextArea',
        'MP.form.Panel',
        'MP.window.Notification'
    ],

    statics: {
        EDIT_ACTION: 'edit_availability'
    },

    initActions: function() {
        var me = this;
        var ids = me.statics();

        me.callParent();

        me.editAction = me.addAction(new Ext.Action({
            itemId: ids.EDIT_ACTION,
            text: _('Modify'),
            tooltip: _('Edit selected availability.'),
            iconCls: 'edit-record-icon',
            disabled: true,
            needsOneSelectedRow: true,
            handler: function() {
                var record = me.component.getSelectionModel().getSelection()[0];
                me.showEditWindow(record);
            }
        }));
    },

    attachActions: function() {
        var me = this;

        me.callParent();

        var tbar = me.component.child('#ttoolbar');

        tbar.add(2, ' ', me.editAction);

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
        var win = desktop.getWindow('edit-availability-win');

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        var metadata = me.module.config.metadata,
            size = desktop.getReasonableWindowSize(600, 250),
            editors = metadata.editors({
                '*': {
                    editor: MP.form.Panel.getDefaultEditorSettingsFunction('100%')
                },
                note: {
                    editor: {
                        xtype: 'textarea'
                    }
                },
                date: {
                    editor: {
                        listeners: {
                            expand: function(event) {
                                var bf = form.getForm(),
                                df = bf.findField(editors.date.name);
                                df.setMinValue(me.module.edition.startdate);
                                df.setMaxValue(me.module.edition.enddate);
                                if(!df.getValue())
                                    df.setValue(me.module.edition.startdate);
                            }
                        }
                    }
                },
                endtime: {
                    editor: {
                        listeners: {
                            beforequery: function(event) {
                                var bf = form.getForm(),
                                    stf = bf.findField(editors.starttime.name),
                                    etf = bf.findField(editors.endtime.name),
                                    st = stf.getValue();
                                etf.setMinValue(st || '07:00');
                            }
                        }
                    }
                },
                starttime: {
                    editor: {
                        listeners: {
                            beforequery: function(event) {
                                var bf = form.getForm(),
                                    stf = bf.findField(editors.starttime.name),
                                    etf = bf.findField(editors.endtime.name),
                                    et = etf.getValue();
                                stf.setMaxValue(et || '23:59');
                            }
                        }
                    }
                }
            }), edit_items = [];

        if(!me.module.single_person)
            edit_items.push(editors.Person);
        edit_items.push({
            xtype: 'container',
            layout: 'hbox',
            items: [{
                xtype: 'container',
                layout: 'anchor',
                flex: 1,
                items: [editors.date]
            }, {
                xtype: 'container',
                layout: 'anchor',
                flex: 1,
                items: [editors.starttime]
            }, {
                xtype: 'container',
                layout: 'anchor',
                flex: 1,
                items: [editors.endtime]
            }]
        });
        edit_items.push(editors.note);

        var form = Ext.create('MP.form.Panel', {
            autoScroll: true,
            fieldDefaults: {
                labelWidth: 60,
                margin: '15 10 0 10'
            },
            items: edit_items,
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
            id: 'edit-availability-win',
            title: _('Edit availability'),
            iconCls: 'edit-availability-icon',
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


Ext.define('HuRM.module.Availabilities', {
    extend: 'MP.desktop.Module',

    requires: [
        'MP.grid.Panel'
    ],

    uses: [
        'HuRM.module.Availabilities.Actions'
    ],

    id: 'availabilities-win',
    iconCls: 'persons-icon',
    launcherText: null,
    launcherTooltip: null,

    config: {
        xtype: 'editable-grid',
        pageSize: 23,
        autoShowAllEditors: false,
        clicksToEdit: 0,
        dataURL: '/data/availabilities',
        sorters: ['lastname', 'firstname', 'date', 'starttime'],
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
                        Ext.create('HuRM.module.Availabilities.Actions', { module: me }),
                    ]
                });
                callback(config);
                me.app.on('logout', function() { delete config.metadata; }, me, { single: true });
            });
        } else {
            callback(config);
        }
    },

    createOrShowWindow: function(edition, person) {
        var me = this,
            desktop = me.app.getDesktop(),
            win = desktop.getWindow(me.id),
            width;

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        if((me.single_person = Ext.isDefined(person))) {
            width = 500;
        }

        me.edition = edition;

        me.configure(
            [me.getConfig],
            function(done) {
                var size = desktop.getReasonableWindowSize(width),
                    config = Ext.apply({
                        stickyFilters: [{
                            id: 'edition',
                            property: 'idedition',
                            value: edition.get('idedition')
                        }],
                        newRecordData: {
                            idedition: edition.get('idedition')
                        }
                    }, me.config),
                    title;

                Ext.each(config.columns, function(col) {
                    if(col.dataIndex == 'Person') {
                        col.hidden = me.single_person;
                        return false;
                    } else
                        return true;
                });

                if(me.single_person) {
                    config.sorters = ['date', 'starttime'];
                    config.newRecordData.idperson = person.get('idperson');
                    config.newRecordData.Person = person.get('FullName');
                    config.stickyFilters.push({
                        id: 'person',
                        property: 'idperson',
                        value: person.get('idperson')
                    });
                    title = Ext.String.format(_("Availability of {0} in edition “{1}”"),
                                              person.get('FullName'),
                                              edition.get('description'));
                } else {
                    title = Ext.String.format(_("Persons willing to cooperate to edition “{0}”"),
                                              edition.get('description'));
                }

                win = desktop.createWindow({
                    id: me.id,
                    title: title,
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
            });
    }
});
