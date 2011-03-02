var engine = {
    init: function() {
        this.tickets();
        this.statuses();
    },
    tickets: function() {
        _this = this;
        $.get('/nezabudka/tickets/', {},
              function(json) {
                  var content = $('#ticket_list');
                  $.each(json, function() {
                      var item = this;
                      var click_handler = function() { _this.show_ticket(item.id); }
                      var dom_object = $('<div/>')
                                       .addClass('listitem')
                                       .text('Ticket '+item.id+': '+  item.title)
                                       .click(click_handler);
                      content.append(dom_object);
                  });
              });
    },
    statuses: function() {
        $.get('/nezabudka/statuses/', {},
              function(json) {
                  var content = $('#selector #status');
                  for (var i=0; i<json.length; i++) {
                      var id = json[i].id,
                          title = json[i].title,
                          item = $('<div/>')
                                   .addClass('listitem')
                                   .text(title)
                                   .click(function() { alert(id) });
                      content.append(item);
                  }
              });
    },
    show_ticket: function(ticket_id) {
        var content = $('#item_info');
        $('div', content).each(function() { $(this).remove(); })
        $.get('/nezabudka/comments/' + ticket_id + '/', {},
              function(json) {
                  for (var i=0; i<json.length; i++) {
                      var id = json[i].id,
                          desc = json[i].text,
                          item = $('<div/>')
                                   .addClass('comment_item')
                                   .text(desc)
                                   .click(function() { alert(id) });
                      content.append(item);
                  }
              });
    }
}

$(document).ready(function() {
    engine.init();
} );
