## -*- coding: utf-8 -*-
<%inherit file="/master/edit.mako" />

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if version_count is not Undefined and request.has_perm('product.versions.view'):
      <li>${h.link_to("View Change History ({})".format(version_count), url('product.versions', uuid=instance.uuid))}</li>
  % endif
</%def>

${parent.body()}
