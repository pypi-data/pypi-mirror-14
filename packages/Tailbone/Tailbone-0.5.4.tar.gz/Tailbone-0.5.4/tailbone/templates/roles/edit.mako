## -*- coding: utf-8 -*-
<%inherit file="/master/edit.mako" />

<%def name="head_tags()">
  ${parent.head_tags()}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/perms.css'))}
</%def>

<%def name="context_menu_items()">
  ${parent.context_menu_items()}
  % if version_count is not Undefined and request.has_perm('role.versions.view'):
      <li>${h.link_to("View Change History ({0})".format(version_count), url('role.versions', uuid=instance.uuid))}</li>
  % endif
</%def>

${parent.body()}
