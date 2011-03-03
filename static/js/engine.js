var engine = {

    window_width: 0,
    window_height: 0,
    ticket_id: 0,

    init: function() {
        var _this = this;
        // resize widgets on load and resize events
        $(window).bind('load resize', function() {
            var w = _this.window_width = $(this).width() - 50;
            var h = _this.window_height = $(this).height() - 50;
            var tds = $('#content table td');
            $(tds[0]).css({width: _this.pct_of_width(w, 0.1)});
            $(tds[1]).css({width: _this.pct_of_width(w, 0.4)});
            $(tds[2]).css({width: _this.pct_of_width(w, 0.5)});
        });
        // load tickets and statuses
        this.tickets();
        this.statuses();
        // action buttons
        $('#action_buttons span').each(function() {
            $(this).click(function() {
                _this.toggle_comment_form(_this.ticket_id);
            });
        });
        _this.setup_comment_form();
    },
    pct_of_width: function(width, percent) {
        return Math.floor(width * percent) + 'px'
    },
    setup_comment_form: function() {
        var _this = this,
            form = $('#add_comment_form'),
            text = $('#comment', form);
        $('#cancel_comment', form).click(function() {
            _this.toggle_comment_form(_this.ticket_id);
        });
        $('#add_comment', form).click(function() {
            $.ajax({
                type: 'POST',
                url: '/nezabudka/comments/add/',
                data: $.param({
                    ticket: _this.ticket_id,
                    text: text.val()
                }),
                success: function(msg) {
                    text.val('');
                    form.addClass('hide');
                    _this.show_ticket(_this.ticket_id);
                    $.jGrowl('Comment added successfully.', { header: 'Comments' });
                },
                error: function(xhr, ajaxOptions, thrownError) {
                    $.jGrowl('Too fast commenting! Wait a little, please.<br/>'
                             + 'Exception: ' + thrownError.toLowerCase(),
                             { header: 'Comment Adding' });
                }
            });
        });
    },
    tickets: function() {
        var _this = this;
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
        var _this = this,
            content = $('#item_info'),
            comments = $('#comment_list');
        _this.ticket_id = ticket_id;
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
                  // show action buttons
                  $('#action_buttons').removeClass('hide');
              });
    },
    toggle_comment_form: function(ticket_id) {
        var _this = this,
            form = $('#add_comment_form'),
            text = $('#comment', form);
        form.css({
            top: _this.window_height/5,
            left: _this.window_width/3,
        }).toggleClass('hide');
    }
}

$(document).ready(function() {
    engine.init();
} );
