## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">New ${model_title}</%def>

<%def name="context_menu_items()">
  % if request.has_perm('{}.list'.format(permission_prefix)):
      <li>${h.link_to("Back to {}".format(model_title_plural), index_url)}</li>
  % endif
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->
