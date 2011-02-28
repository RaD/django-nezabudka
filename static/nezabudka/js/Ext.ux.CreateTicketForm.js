Ext.ux.CreateTicketForm = Ext.extend(Ext.form.FormPanel, {
    initComponent: function(){
        var config = {
            clientValidation: true,
            paramsAsHash: true,
            api: {
                submit: TicketApi.create
            },
            items: []
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.CreateTicketForm.superclass.initComponent.call(this);
    }
});

