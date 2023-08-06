## -*- coding: utf-8 -*-
<%inherit file="/master/view.mako" />

<%def name="title()">${model_title}</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Back to {}".format(batch_model_title), index_url)}</li>
  % if master.rows_editable and instance_editable and request.has_perm('{}.edit'.format(permission_prefix)):
      <li>${h.link_to("Edit this {}".format(model_title), action_url('edit', instance))}</li>
  % endif
  % if master.rows_deletable and instance_deletable and request.has_perm('{}.delete'.format(permission_prefix)):
      <li>${h.link_to("Delete this {}".format(model_title), action_url('delete', instance))}</li>
  % endif
  % if master.rows_creatable and request.has_perm('{}.create'.format(permission_prefix)):
      <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
  % endif
</%def>

${parent.body()}
