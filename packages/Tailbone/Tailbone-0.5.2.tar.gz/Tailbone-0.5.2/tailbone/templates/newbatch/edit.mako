## -*- coding: utf-8 -*-
<%inherit file="/master/edit.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.js'))}
  <script type="text/javascript">
    $(function() {

        $('.newgrid-wrapper').gridwrapper();

        $('#save-refresh').click(function() {
            var form = $(this).parents('form');
            form.append($('<input type="hidden" name="refresh" value="true" />'));
            form.submit();
        });

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

<%def name="buttons()">
    <div class="buttons">
      % if master.refreshable:
          ${h.submit('save-refresh', "Save & Refresh Data")}
      % endif
      % if not batch.executed and request.has_perm('{}.execute'.format(permission_prefix)):
          <button type="button" id="execute-batch"${'' if execute_enabled else ' disabled="disabled"'}>${execute_title}</button>
      % endif
    </div>
</%def>

<%def name="grid_tools()">
    % if not batch.executed:
        <p>${h.link_to("Delete all rows matching current search", url('{}.rows.bulk_delete'.format(route_prefix), uuid=batch.uuid))}</p>
    % endif
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render(buttons=capture(buttons))|n}
</div><!-- form-wrapper -->

${rows_grid.render_complete(allow_save_defaults=False, tools=capture(self.grid_tools))|n}
