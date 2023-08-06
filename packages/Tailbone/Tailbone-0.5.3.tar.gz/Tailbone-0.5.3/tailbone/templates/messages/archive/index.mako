## -*- coding: utf-8 -*-
<%inherit file="/messages/index.mako" />

<%def name="title()">Message Archive</%def>

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">
    destination = "Inbox";
  </script>
</%def>

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  <li>${h.link_to("Go to my Message Inbox", url('messages.inbox'))}</li>
  <li>${h.link_to("Go to my Sent Messages", url('messages.sent'))}</li>
</%def>

<%def name="grid_tools()">
  ${h.form(url('messages.move_bulk'), name='move-selected')}
    ${h.hidden('destination', value='inbox')}
    ${h.hidden('uuids')}
    <button type="submit">Move 0 selected to Inbox</button>
  ${h.end_form()}
</%def>

${parent.body()}
