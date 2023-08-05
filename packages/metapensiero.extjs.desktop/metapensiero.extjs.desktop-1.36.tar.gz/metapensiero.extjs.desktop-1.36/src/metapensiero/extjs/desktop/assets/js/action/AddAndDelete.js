// -*- coding: utf-8 -*-
// :Project:   metapensiero.extjs.desktop -- Standard "add" and "delete" actions.
// :Created:   lun 26 nov 2012 15:42:08 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2012, 2013, 2016 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare _*/


Ext.define('MP.action.AddAndDelete', {
    extend: 'MP.action.StoreAware',
    uses: ['Ext.Action'],

    statics: {
        ADD_ACTION: 'add',
        DELETE_ACTION: 'delete'
    },

    initActions: function() {
        var me = this;
        var ids = me.statics();

        me.callParent();

        var grid = me.component;

        me.addNewRecordAction = me.addAction(new Ext.Action({
            itemId: ids.ADD_ACTION,
            text: _('Add new'),
            tooltip: _('Create a new record.'),
            iconCls: 'mp-add-action-icon',
            handler: grid.addRecord,
            scope: grid
        }));

        me.deleteRecordAction = me.addAction(new Ext.Action({
            itemId: ids.DELETE_ACTION,
            text: _('Delete'),
            tooltip: _('Delete selected record.'),
            iconCls: 'mp-delete-action-icon',
            disabled: true,
            needsSelectedRow: true,
            scope: grid,
            handler: grid.deleteRecord
        }));
    }
});
