var engine = {

    window_width: 0,

    init: function() {
        _this = this;
        $(window).bind('load resize', function() {
            _this.window_width = w = $(this).width() - 50;
            tds = $('#content table td');
            $(tds[0]).css({width: _this.pct_of_width(w, 0.1)});
            $(tds[1]).css({width: _this.pct_of_width(w, 0.4)});
            $(tds[2]).css({width: _this.pct_of_width(w, 0.5)});
        });
        this.tickets();
        this.statuses();
    },
    pct_of_width: function(width, percent) {
        return Math.floor(width * percent) + 'px'
    },
    tickets: function() {
        _this = this;
        $.get('/nezabudka/tickets/', {},
              function(json) {
                  var content = $('#ticket_list'),
                      _width = content.width();
                  $.each(json, function() {
                      var item = this;
                      var click_handler = function() { _this.show_ticket(item.id); }
                      var div = $('<div/>').addClass('listitem').click(click_handler)
                      .text('Ticket '+item.id+': '+  item.title)
                      .attr({alt: item.title, title: item.title})
                      .css({width: (_width - 4) + 'px'});
                      content.append(div);
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
                                   .addClass('selector_item')
                                   .text(title)
                                   .click(function() { alert(id) });
                      content.append(item);
                  }
              });
    },
    show_ticket: function(ticket_id) {
        _this = this;
        var content = $('#item_info');
        var comments = $('#comment_list');
        $.get('/nezabudka/comments/' + ticket_id + '/', {},
              function(json) {
                  $('#title', content).text(json.ticket.title);
                  $('#component > span', content).text(json.ticket.component_title);

                  $('div', comments).each(function() { $(this).remove(); })
                  $.each(json.comments, function() {
                      header = $('<div/>').html('<b>' + this.user + '</b> @ '
                                                + '<b>' + this.date + '</b><br/>'
                                                + this.text);
                      comments.append($('<div/>')
                                      .append(header)
                                      .addClass('comment_item')
                                      .css({width: _this.pct_of_width(_this.window_width, 0.45)})
                                     );
                  });
              });
    }
}

$(document).ready(function() {
    engine.init();
} );
