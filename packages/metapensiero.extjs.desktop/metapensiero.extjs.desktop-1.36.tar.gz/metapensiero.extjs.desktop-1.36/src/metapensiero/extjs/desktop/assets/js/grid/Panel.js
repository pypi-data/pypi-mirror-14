// -*- coding: utf-8 -*-
// :Project:   metapensiero.extjs.desktop -- Standard editable grid
// :Created:   dom 23 set 2012 17:56:02 CEST
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2012, 2013, 2016 Lele Gaifax
//

/*jsl:declare Ext*/


Ext.define('MP.grid.Panel', {
    extend: 'MP.grid.Editable',

    uses: ['MP.action.AddAndDeleteOnToolbar'],

    alias: 'widget.editable-grid',

    initComponent: function() {
        var me = this;

        me.callParent();

        if(!me.noAddAndDelete) {
            this.plugins.unshift(Ext.create('MP.action.AddAndDeleteOnToolbar'));
        }
    }
});
