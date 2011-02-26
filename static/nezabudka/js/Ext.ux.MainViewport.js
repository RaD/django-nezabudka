Ext.ux.MainViewport = Ext.extend(Ext.Viewport, {
    public_attr: 1,
    renderTo: Ext.getBody(),
    initComponent: function(){
        var config = {
            private_attr: 2,
            layout: 'border',
            defaults: {
                frame: true
            },
            items: [{
                region: 'center',
                xtype: 'ext:ux:tickets-grid'
            },{
                region: 'east',
                width: 350,
                html: 'Hello!',
            },{
                region: 'north',
                contentEl: 'header',
                height: 40                
            }]
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.MainViewport.superclass.initComponent.apply(this, arguments);
    }//initComponent                  
});