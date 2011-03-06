var engine = {

    window_width: 0,
    window_height: 0,
    ticket_id: 0,
    form_widget: false,
    form_dom: false,

    init: function() {
        var _this = this;
        _this.form_widget = $('#form_widget');
        _this.form_dom = $('form', _this.form_widget);

        // resize widgets on load and resize events
        $(window).bind('load resize', function() {
            var w = _this.window_width = $(this).width() - 50;
            var h = _this.window_height = $(this).height() - 50;
            var tds = $('#content table td');
            $(tds[0]).css({width: _this.pct_of_width(w, 0.1)});
            $(tds[1]).css({width: _this.pct_of_width(w, 0.4)});
            $(tds[2]).css({width: _this.pct_of_width(w, 0.5)});
        });

        // buttons
        var actions = $('#action_buttons');
        _this.init_ticket_new();
        _this.reinit_action_buttons(actions);

        // form buttons
        $('input[type="reset"]', _this.form_dom).click(function() {
            _this.toggle_widget(_this.form_widget);
        });

        // load tickets and statuses
        this.update_tickets();
        this.statuses();
    },
    reinit_action_buttons: function(actions) {
        var _this = this;
        $('#add_comment', actions)
          .unbind('click')
          .click(
              function() {
                  console.log('add_comment');
                  _this.toggle_widget(_this.form_widget);
              });

        _this.init_status_change(actions);
    },
    init_ticket_new: function() {
        var _this = this;
        // new ticket button
        $('#new_ticket').click(function() {
            $.get('/nezabudka/ticket/', {},
                  function(json) {
                      var header = 'New Ticket',
                          title = $('#title', _this.form_widget).html(header);
                      $(_this.form_dom).attr({method: 'post', action: json.action})
                                       .unbind('submit')
                                       .submit(function() {
                                           _this.submit_form(_this.form_dom, header,
                                                             function(msg) {
                                                                 _this.form_widget.addClass('hide');
                                                                 _this.update_tickets();
                                                                 $.jGrowl('Ticket added successfully.', { header: header });
                                                             });
                                           return false;
                                       });
                      $('#container', _this.form_widget).empty().append(json.form);
                      _this.toggle_widget(_this.form_widget);
                  });
        });
    },
    init_status_change: function(actions) {
        var _this = this;
        $('#change_status', actions)
        .unbind('click')
        .click(
            function() {
                $.get('/nezabudka/status/' + _this.ticket_id + '/', {},
                      function(json) {
                          var header = 'Ticket\' Status',
                              title = $('#title', _this.form_widget).html(header);
                          // get the form description from server and insert into page's DOM
                          $('#container', _this.form_widget).empty().append(json.form);
                          // add submit handler
                          $(_this.form_dom)
                          .attr({method: 'put', action: json.action})
                          .unbind('submit')
                          .submit(function() {
                              _this.submit_form(_this.form_dom, header,
                                                function(msg) {
                                                    _this.form_widget.addClass('hide');
                                                    _this.show_ticket(_this.ticket_id);
                                                    $.jGrowl('Status changed.', { header: header });
                                                });
                              return false;
                          });
                          // show the form
                          _this.toggle_widget(_this.form_widget);
                      });
            });
    },
    pct_of_width: function(width, percent) {
        return Math.floor(width * percent) + 'px'
    },
    toggle_widget: function(widget) {
        widget.css({
            top: this.window_height/5,
            left: this.window_width/3,
        }).toggleClass('hide');
    },
    submit_form: function(form, title, callback_success) {
        var _this = this;
        $.ajax({type: form.attr('method'), url: form.attr('action'), data: form.formSerialize(),
                success: callback_success,
                error: function(xhr, ajaxOptions, thrownError) {
                    $.jGrowl.error('Response: ' + xhr.responseText + '<br/>' +
                                   'Exception: ' + thrownError.toLowerCase(),
                                   { header: title });
                }
               });
    },
    update_tickets: function() {
        var _this = this;
        $.get('/nezabudka/tickets/', {},
              function(json) {
                  var content = $('#ticket_list'),
                      _width = content.width();
                  content.empty();
                  $.each(json, function() {
                      var item = this;
                      var click_handler = function() { _this.show_ticket(item.id); }
                      var div = $('<div/>').addClass('listitem').click(click_handler)
                      .text('#'+item.id+': '+  item.title)
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
                  // clear up
                  $(_this.form_dom).unbind('submit');
                  comments.empty();

                  // fill the ticket panel
                  $('#title', content).text(json.ticket.title);
                  $('#component > span', content).text(json.ticket.component_title);
                  $('#status > span', content).text(json.ticket.status_title);

                  // show comments' history
                  $.each(json.comments, function() {
                      header = $('<div/>').html('<b>' + this.user + '</b> @ '
                                                + '<b>' + this.date + '</b><br/>'
                                                + '<pre>' + this.text + '</pre>');
                      comments.append($('<div/>')
                                      .append(header)
                                      .addClass('comment_item')
                                      .css({width: _this.pct_of_width(_this.window_width, 0.45)})
                                     );
                  });
                  // show action buttons
                  $('#action_buttons').removeClass('hide');
                  // prepare comment form
                  var header = 'Comment',
                      title = $('#title', _this.form_widget).html(header);
                  $(_this.form_dom).attr({method: 'post', action: json.action})
                                   .unbind('submit')
                                   .submit(function() {
                                       _this.submit_form(_this.form_dom, header,
                                                         function(msg) {
                                                             _this.form_widget.addClass('hide');
                                                             _this.show_ticket(_this.ticket_id);
                                                             $.jGrowl('Comment added successfully.', { header: header });
                                                         });
                                       return false;
                                   });
                  // form content itself
                  $('#container', _this.form_widget).empty().append(json.form);
              });
    }
}

$(document).ready(function() {
    engine.init();
} );
