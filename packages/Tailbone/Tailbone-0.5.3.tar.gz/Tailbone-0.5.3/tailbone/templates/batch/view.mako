## -*- coding: utf-8 -*-
<%inherit file="/batch/crud.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  <script type="text/javascript">
    $(function() {
        $('#execute-batch').click(function() {
            $(this).button('option', 'label', "Executing, please wait...").button('disable');
            location.href = '${url('{0}.execute'.format(route_prefix), uuid=batch.uuid)}';
        });
    });
  </script>
</%def>

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('{0}.csv'.format(permission_prefix)):
      <li>${h.link_to("Download this {0} as CSV".format(batch_display), url('{0}.csv'.format(route_prefix), uuid=batch.uuid))}</li>
  % endif
</%def>

<%def name="buttons()">
    <div class="buttons">
      % if not form.readonly and batch.refreshable:
          ${h.submit('save-refresh', "Save & Refresh Data")}
      % endif
      % if not batch.executed and request.has_perm('{0}.execute'.format(permission_prefix)):
          <button type="button" id="execute-batch"${'' if execute_enabled else ' disabled="disabled"'}>${execute_title}</button>
      % endif
    </div>
</%def>

${parent.body()}
