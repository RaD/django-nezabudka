Ext.ns('Ext.ux.stores');

Ext.ux.stores.TicketStore = new Ext.data.DirectStore({
    root: 'data',
    storeId: 'tickets-store',
    totalProperty: 'count',
    autoLoad: true,
    fields: [
        'id',
        'title',
        'user',
        'created',
        'project',
        'component',
        'category',
        'assignedTo',
        'priority',
        'severity',
        'status'
    ],
    api: {
        read: TicketApi.read
    }      
});

Ext.ux.TicketGrid = Ext.extend(Ext.grid.GridPanel, {
    id: 'tickets-grid',
    frame: true,
    loadMask: {msg: 'Loading Tickets...'},
    initComponent: function(){
        var config = {
            store: 'tickets-store',
            sm: new Ext.grid.RowSelectionModel({
                singleSelect:true
            }),
            viewConfig: {
                forceFit: true,
                enableRowBody: true,
                showPreview: true,
                getRowClass: function(record, rowIndex, rp, ds){ // rp = rowParams
                    if(this.showPreview){
                        rp.body = '<p>'+
                            '<b>Project:</b> '+record.get('project')+
                            '<b>Created:</b> '+record.get('created')+'<br/>'+
                            '<b>Created by:</b> '+record.get('user')+
                            '<b>Component:</b> '+record.get('component')+'<br/>'+
                            '<b>Category:</b> '+record.get('category')+
                        '</p>';
                        return 'x-grid3-row-expanded';
                    }
                    return 'x-grid3-row-collapsed';
                }
            },
            colModel: new Ext.grid.ColumnModel({
                defaults: {
                    sortable: true,
                    width: 100,
                },
                columns: [{
                    id: 'title',
                    header: 'Title',
                    dataIndex: 'title',
                    width: 300
                }, {
                    id: 'assigned_to',
                    header: 'Assigned to',
                    dataIndex: 'assignedTo'
                },{
                    id: 'priority',
                    header: 'Priority',
                    dataIndex: 'priority'                    
                },{
                    id: 'severity',
                    header: 'Severity',
                    dataIndex: 'severity'                    
                },{
                    id: 'status',
                    header: 'Status',
                    dataIndex: 'status'                    
                }]
            }),
            tbar: [{
                text: 'Add',
                handler: function(){
                    Ext.ux.msg('Add ticket', 'TODO', Ext.Msg.INFO);
                },
                scope: this
            }],
            bbar: new Ext.PagingToolbar({
                store: 'tickets-store',
                displayInfo: true,
                pageSize: TICKETS_ON_PAGE
            })              
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.TicketGrid.superclass.initComponent.call(this);
        this.on('rowdblclick', this.onRowDblClick, this);
    },
    onRowDblClick: function(grid, rowIndex){
        var record = this.getStore().getAt(rowIndex);
        Ext.getCmp('ticket-panel').setTicket(record);
    }
});

Ext.reg('ext:ux:tickets-grid', Ext.ux.TicketGrid);