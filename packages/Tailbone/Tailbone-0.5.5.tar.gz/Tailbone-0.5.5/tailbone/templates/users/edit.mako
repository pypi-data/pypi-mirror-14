## -*- coding: utf-8 -*-
<%inherit file="/master/edit.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if version_count is not Undefined and request.has_perm('user.versions.view'):
      <li>${h.link_to("View Change History ({0})".format(version_count), url('user.versions', uuid=instance.uuid))}</li>
  % endif
</%def>

${parent.body()}
