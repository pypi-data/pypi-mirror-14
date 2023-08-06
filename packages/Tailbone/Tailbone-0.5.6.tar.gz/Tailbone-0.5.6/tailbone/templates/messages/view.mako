## -*- coding: utf-8 -*-
<%inherit file="/master/view.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <style type="text/css">
    .message-tools {
        margin-bottom: 15px;
    }
    .message-body {
        border-top: 1px solid black;
        border-bottom: 1px solid black;
        margin-bottom: 15px;
        white-space: pre-line;
    }
    .message-body p {
        margin-bottom: 15px;
    }
  </style>
</%def>

<%def name="context_menu_items()">
  % if request.has_perm('messages.create'):
      <li>${h.link_to("Send a new Message", url('messages.create'))}</li>
  % endif
  % if recipient:
      % if recipient.status == rattail.enum.MESSAGE_STATUS_INBOX:
          <li>${h.link_to("Back to Message Inbox", url('messages.inbox'))}</li>
          <li>${h.link_to("Go to my Message Archive", url('messages.archive'))}</li>
          <li>${h.link_to("Go to my Sent Messages", url('messages.sent'))}</li>
      % else:
          <li>${h.link_to("Back to Message Archive", url('messages.archive'))}</li>
          <li>${h.link_to("Go to my Message Inbox", url('messages.inbox'))}</li>
          <li>${h.link_to("Go to my Sent Messages", url('messages.sent'))}</li>
      % endif
  % else:
      <li>${h.link_to("Back to Sent Messages", url('messages.sent'))}</li>
      <li>${h.link_to("Go to my Message Inbox", url('messages.inbox'))}</li>
      <li>${h.link_to("Go to my Message Archive", url('messages.archive'))}</li>
  % endif
</%def>

<%def name="message_tools()">
  % if recipient:
    <div class="message-tools">
      % if request.has_perm('messages.create'):
        ${h.link_to("Reply", url('messages.reply', uuid=instance.uuid), class_='button')}
        ${h.link_to("Reply to All", url('messages.reply_all', uuid=instance.uuid), class_='button')}
      % endif
      % if recipient.status == rattail.enum.MESSAGE_STATUS_INBOX:
        ${h.link_to("Move to Archive", url('messages.move', uuid=instance.uuid) + '?dest=archive', class_='button')}
      % else:
        ${h.link_to("Move to Inbox", url('messages.move', uuid=instance.uuid) + '?dest=inbox', class_='button')}
      % endif
    </div>
  % endif
</%def>

<%def name="message_body()">
  ${instance.body}
</%def>

${parent.body()}

${self.message_tools()}

<div class="message-body">
  ${self.message_body()}
</div>

${self.message_tools()}
