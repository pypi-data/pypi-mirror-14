// -*- coding: utf-8 -*-
// :Project:   metapensiero.extjs.desktop -- "save" and "restore" on the top toolbar
// :Created:   lun 26 nov 2012 15:39:34 CET
// :Author:    Lele Gaifax <lele@metapensiero.it>
// :License:   GNU General Public License version 3 or later
// :Copyright: © 2012, 2016 Lele Gaifax
//

/*jsl:declare Ext*/
/*jsl:declare MP*/


Ext.define('MP.action.SaveAndResetOnToolbar', {
    extend: 'MP.action.Plugin',
    uses: ['MP.action.SaveAndReset'],

    attachActions: function() {
        var me = this, tbar;
        var sandr = MP.action.SaveAndReset;

        me.callParent();

        tbar = me.component.child('#ttoolbar');

        if(tbar) {
            var saction = me.component.findActionById(sandr.SAVE_ACTION);
            var raction = me.component.findActionById(sandr.RESTORE_ACTION);
            tbar.add('->');
            tbar.add(saction);
            tbar.add(raction);
        }
    }
});
