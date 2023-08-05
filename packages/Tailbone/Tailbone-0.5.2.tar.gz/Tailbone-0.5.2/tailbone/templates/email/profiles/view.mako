## -*- coding: utf-8 -*-
<%inherit file="/master/view.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">
    % if not email.get_template('html'):
      $(function() {
          $('#preview-html').button('disable');
          $('#preview-html').attr('title', "There is no HTML template on file for this email.");
      });
    % endif
    % if not email.get_template('txt'):
      $(function() {
          $('#preview-txt').button('disable');
          $('#preview-txt').attr('title', "There is no TXT template on file for this email.");
      });
    % endif
  </script>
</%def>

${parent.body()}

<form action="${url('email.preview')}" name="send-email-preview" method="post">
  <a id="preview-html" class="button" href="${url('email.preview')}?key=${instance['key']}&amp;type=html" target="_blank">Preview HTML</a>
  <a id="preview-txt" class="button" href="${url('email.preview')}?key=${instance['key']}&amp;type=txt" target="_blank">Preview TXT</a>
  or
  <input type="text" name="recipient" value="${request.user.email_address}" />
  <input type="submit" name="send_${instance['key']}" value="Send Preview Email" />
</form>
