## -*- coding: utf-8 -*-
## ##############################################################################
## 
## Default master 'index' template.  Features a prominent data table and
## exposes a way to filter and sort the data, etc.  Some index pages also
## include a "tools" section, just above the grid on the right.
## 
## ##############################################################################
<%inherit file="/base.mako" />

<%def name="title()">${grid.model_title_plural}</%def>

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.javascript_link(request.static_url('tailbone:static/js/jquery.ui.tailbone.js'))}
  <script type="text/javascript">
    $(function() {
        $('.newgrid-wrapper').gridwrapper();
    });
  </script>
</%def>

<%def name="context_menu_items()">
  % if master.creatable and request.has_perm('{}.create'.format(grid.permission_prefix)):
      <li>${h.link_to("Create a new {}".format(grid.model_title), url('{}.create'.format(grid.route_prefix)))}</li>
  % endif
</%def>

<%def name="grid_tools()"></%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

${grid.render_complete(tools=capture(self.grid_tools))|n}
