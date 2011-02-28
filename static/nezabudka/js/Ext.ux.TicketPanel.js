Ext.ux.TicketInfoPanel = Ext.extend(Ext.Panel, {
    html: '',
    tpl: new Ext.XTemplate(
        'Project: {project}<br/>',
        'Category: {category}<br/>',
        'Component: {component}<br/>',
        'Created by: {created_by}<br/>',
        'Created: {created}<br/>'
    )    
});

Ext.ux.TicketCommentsPanel = Ext.extend(Ext.Panel, {
    html: ''
});

Ext.ux.TicketPanel = Ext.extend(Ext.Panel, {
    id: 'ticket-panel',
    frame: true,
    title: 'Select ticket with double-click',
    initComponent: function(){
        var config = {
            layout: 'vbox',
            items: [
                new Ext.ux.TicketInfoPanel({
                    flex: 1
                }),
                new Ext.ux.TicketCommentsPanel({
                    flex: 1
                })
            ]
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.TicketPanel.superclass.initComponent.call(this);
    },
    setTicket: function(record){
        console.log(this.items, this.items.get(0))
        this.items.get(0).update(record.data);
        this.setTitle(record.get('title'));
    }
});

Ext.reg('ext:ux:ticket-panel', Ext.ux.TicketPanel);
