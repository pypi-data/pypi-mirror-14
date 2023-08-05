// -*- coding: utf-8 -*-
// :Project:   hurm -- Duties management windows
// :Created:   mer 03 feb 2016 21:23:56 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2016 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare HuRM*/
/*jsl:declare MP*/
/*jsl:declare _*/
/*jsl:declare ngettext*/

Ext.define('HuRM.module.Duties.Actions', {
    extend: 'MP.action.StoreAware',

    uses: [
        'Ext.Action',
        'Ext.form.field.TextArea',
        'MP.form.Panel',
        'MP.window.Notification'
    ],

    statics: {
        EDIT_ACTION: 'edit_duty'
    },

    initActions: function() {
        var me = this;
        var ids = me.statics();

        me.callParent();

        me.editAction = me.addAction(new Ext.Action({
            itemId: ids.EDIT_ACTION,
            text: _('Modify'),
            tooltip: _('Edit selected duty.'),
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
        var me = this,
            desktop = me.module.app.getDesktop(),
            win = desktop.getWindow('edit-duty-win');

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        MP.desktop.App.request(
            'GET', '/data/duty_payloads',
            {sort: 'description',
             filter_idduty: record.get('idduty'),
             result: 'payloads',
             count: false},
            function(result) {
                var metadata = me.module.config.metadata,
                    size = desktop.getReasonableWindowSize(640, 320),
                    orig_url,
                    editors = metadata.editors({
                        '*': {
                            editor: MP.form.Panel.getDefaultEditorSettingsFunction('100%')
                        },
                        Person: {
                            editor: {
                                listeners: {
                                    beforequery: function(event) {
                                        var store = event.combo.store,
                                        idtask = record.get('idtask');
                                        if(!orig_url)
                                            orig_url = store.proxy.url;
                                        store.proxy.url = Ext.String.urlAppend(orig_url,
                                                                               'idtask='+idtask);
                                        delete event.combo.lastQuery;
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
                        note: {
                            editor: {
                                xtype: 'textarea'
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
                    }),
                    items = [editors.Person,
                             editors.starttime,
                             editors.endtime],
                    leftcol = [],
                    rightcol = [],
                    payload_field_names = [];

                items.push({
                        xtype: 'container',
                        layout: 'hbox',
                        items: [{
                            xtype: 'container',
                            layout: 'anchor',
                            flex: 1,
                            items: leftcol
                        }, {
                            xtype: 'container',
                            layout: 'anchor',
                            flex: 1,
                            items: rightcol
                        }]
                });

                for(var i = 0, l = result.payloads.length; i < l; i++) {
                    var payload = result.payloads[i],
                        idap = payload.idactivitypayload + '',
                        name = 'idactivitypayload_' + idap;

                    payload_field_names.push(name);
                    (i % 2 == 0 ? leftcol : rightcol).push({
                        xtype: 'numberfield',
                        fieldLabel: payload.description,
                        anchor: '100%',
                        name: name,
                        minValue: 0,
                        value: payload.value,
                        plugins: [{ptype: 'fieldhint', text: payload.note}]
                    });
                }

                size.height += 45 * payload_field_names.length / 2;

                items.push(editors.note);

                var form = Ext.create('MP.form.Panel', {
                    autoScroll: true,
                    fieldDefaults: {
                        labelWidth: 100,
                        margin: '15 10 0 10'
                    },
                    items: items,
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
                                var fvalues = form.getValues(),
                                    payloads = [];

                                form.updateRecord(record);

                                for(var i = 0, l = payload_field_names.length; i < l; i++) {
                                    var fname = payload_field_names[i],
                                        value = fvalues[fname];
                                    if(value)
                                        payloads.push({
                                            idactivitypayload: parseInt(fname.split('_')[1]),
                                            value: parseInt(value)
                                        });
                                }

                                record.set('payloads', payloads);

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
                    id: 'edit-duty-win',
                    title: _('Edit duty'),
                    iconCls: 'edit-duty-icon',
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
            });
    }
});


Ext.define('HuRM.module.Duties', {
    extend: 'MP.desktop.Module',

    requires: [
        'MP.grid.Panel'
    ],

    uses: [
        'HuRM.module.Duties.Actions'
    ],

    id: 'duties-win',
    iconCls: 'duties-icon',
    launcherText: null,
    launcherTooltip: null,

    config: {
        xtype: 'editable-grid',
        pageSize: 15,
        autoShowAllEditors: false,
        clicksToEdit: 0,
        dataURL: '/data/duties',
        sorters: ['date', 'starttime', 'Person'],
        stripeRows: true
    },

    getConfig: function(callback) {
        var me = this,
            config = me.config;

        if(!config.metadata) {
            MP.data.MetaData.fetch(config.dataURL, me, function(metadata) {
                var overrides = me.getFocusedGridOverrides(),
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
                        Ext.create('HuRM.module.Duties.Actions', { module: me }),
                    ]
                });
                callback(config);
                me.app.on('logout', function() { delete config.metadata; }, me, { single: true });
            });
        } else {
            callback(config);
        }
    },

    createOrShowWindow: function(edition, focus) {
        var me = this,
            desktop = me.app.getDesktop(),
            win = desktop.getWindow(me.id);

        // If the window is already present, destroy and recreate it,
        // to reapply configuration and filters
        if(win) {
            win.destroy();
        }

        me.edition = edition;
        me.focus = focus;

        me.configure(
            [me.getConfig],
            function(done) {
                var size = desktop.getReasonableWindowSize(720, 520),
                    config = Ext.apply(me.getFocusedConfig(), me.config),
                    title = me.getFocusedTitle();

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

                me.configureActionsForFocus(grid);
            });
    },

    getFocusedConfig: function() {
        var me = this,
            task = me.focus;

        return {
            stickyFilters: [{
                id: 'task',
                property: 'idtask',
                value: task.get('idtask')
            }],
            newRecordData: {
                idtask: task.get('idtask')
            }
        };
    },

    getFocusedTitle: function() {
        var me = this,
            task = me.focus,
            npersonsmsg = Ext.String.format(
                ngettext('{0} person', '{0} persons', task.get('npersons')),
                task.get('npersons'));

        return Ext.String.format(
            // TRANSLATORS: this is the title of the duties
            // window, params are activity, location, starttime,
            // endtime, date and number of persons.
            _("Duties for activity “{0}” at “{1}” from {2} to {3} on {4}, {5}"),
            task.get('Activity'),
            task.get('Location'),
            Ext.Date.format(task.get('starttime'), _('g:i A')),
            Ext.Date.format(task.get('endtime'), _('g:i A')),
            Ext.Date.format(task.get('date'), _('m/j/Y')),
            npersonsmsg);
    },

    getFocusedGridOverrides: function() {
        return {};
    },

    configureActionsForFocus: function(grid) {
    }
});
