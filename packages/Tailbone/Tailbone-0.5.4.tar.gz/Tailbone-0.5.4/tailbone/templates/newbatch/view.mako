## -*- coding: utf-8 -*-
<%inherit file="/master/view.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.js'))}
  <script type="text/javascript">
    $(function() {

        $('.newgrid-wrapper').gridwrapper();

        $('#execute-batch').click(function() {
            $(this).button('option', 'label', "Executing, please wait...").button('disable');
            location.href = '${url('{}.execute'.format(route_prefix), uuid=batch.uuid)}';
        });

    });
  </script>
  <style type="text/css">

    .newgrid-wrapper {
        margin-top: 10px;
    }
    
  </style>
</%def>

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if request.has_perm('{}.csv'.format(permission_prefix)):
      <li>${h.link_to("Download row data as CSV", url('{}.csv'.format(route_prefix), uuid=batch.uuid))}</li>
  % endif
</%def>

<%def name="buttons()">
    <div class="buttons">
      % if not form.readonly and batch.refreshable:
          ${h.submit('save-refresh', "Save & Refresh Data")}
      % endif
      % if not batch.executed and request.has_perm('{}.execute'.format(permission_prefix)):
          <button type="button" id="execute-batch"${'' if execute_enabled else ' disabled="disabled"'}>${execute_title}</button>
      % endif
    </div>
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render(form_id='batch-form', buttons=capture(buttons))|n}
</div><!-- form-wrapper -->

${rows_grid|n}
