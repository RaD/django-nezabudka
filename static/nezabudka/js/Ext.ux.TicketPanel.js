Ext.ux.TicketPanel = Ext.extend(Ext.Panel, {
    id: 'ticket-panel',
    html: '',
    frame: true,
    tpl: new Ext.XTemplate(
        '<h2>{title}</h2>'
    )
});

Ext.reg('ext:ux:ticket-panel', Ext.ux.TicketPanel);
