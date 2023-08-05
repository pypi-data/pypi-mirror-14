## -*- coding: utf-8 -*-
<%inherit file="/master/create.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.javascript_link(request.static_url('tailbone:static/js/lib/tag-it.min.js'))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/jquery.tagit.css'))}
  <script type="text/javascript">

    var recipient_mappings = new Map([
        <% last = len(available_recipients) %>
        % for i, (uuid, entry) in enumerate(sorted(available_recipients.iteritems(), key=lambda r: r[1]), 1):
            ['${uuid}', ${json.dumps(entry)|n}]${',' if i < last else ''}
        % endfor
    ]);

    $(function() {

        var recipients = $('.recipients input');

        recipients.tagit({

            autocomplete: {
                delay: 0,
                minLength: 2,
                autoFocus: true,
                removeConfirmation: true,

                source: function(request, response) {
                    var term = request.term.toLowerCase();
                    var data = [];
                    recipient_mappings.forEach(function(name, uuid) {
                        if (!name.toLowerCase && name.name) {
                            name = name.name;
                        }
                        if (name.toLowerCase().indexOf(term) >= 0) {
                            data.push({value: uuid, label: name});
                        }
                    });
                    response(data);
                }
            },

            beforeTagAdded: ${self.before_tag_added()},

            beforeTagRemoved: function(event, ui) {

                // Unfortunately we're responsible for cleaning up the hidden
                // field, since the values there do not match the tag labels.
                var tags = recipients.tagit('assignedTags');
                var uuid = ui.tag.data('uuid');
                tags = tags.filter(function(element) {
                    return element != uuid;
                });
                recipients.data('ui-tagit')._updateSingleTagsField(tags);
            }
        });

        // set focus to recipients field
        recipients.data('ui-tagit').tagInput.focus();

    });
  </script>
  <style type="text/css">

    .field-wrapper.subject .field input[type="text"],
    .field-wrapper.body .field textarea {
        width: 99%;
    }

  </style>
</%def>

<%def name="before_tag_added()">
    function(event, ui) {

        // Lookup the name in cached mapping, and show that on the tag, instead
        // of the UUID.  The tagit widget should take care of keeping the
        // hidden field in sync for us, still using the UUID.
        var uuid = ui.tagLabel;
        var name = recipient_mappings.get(uuid);
        ui.tag.find('.tagit-label').html(name);
    }
</%def>

<%def name="context_menu_items()">
  % if request.has_perm('messages.list'):
      <li>${h.link_to("Go to my Message Inbox", url('messages.inbox'))}</li>
      <li>${h.link_to("Go to my Message Archive", url('messages.archive'))}</li>
      <li>${h.link_to("Go to my Sent Messages", url('messages.sent'))}</li>
  % endif
</%def>

${parent.body()}
