## -*- coding: utf-8 -*-
<%inherit file="/base.mako" />

<%def name="title()">Delete ${model_title}: ${instance_title}</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Back to {}".format(model_title_plural), url(route_prefix))}</li>
  % if master.viewable and request.has_perm('{}.view'.format(permission_prefix)):
      <li>${h.link_to("View this {}".format(model_title), action_url('view', instance))}</li>
  % endif
  % if master.editable and request.has_perm('{}.edit'.format(permission_prefix)):
      <li>${h.link_to("Edit this {}".format(model_title), action_url('edit', instance))}</li>
  % endif
  % if master.creatable and request.has_perm('{}.create'.format(permission_prefix)):
      <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
  % endif
</%def>

<%def name="confirmation()">
  <br />
  <p>Are you sure about this?</p>

  ${h.form(request.current_route_url())}
    <div class="buttons">
      <button type="button" onclick="$(this).parents('form').submit();">Yes, please DELETE this record forever!</button>
      <a class="button" href="${form.cancel_url}">Whoops, nevermind...</a>
    </div>
  ${h.end_form()}
</%def>

<ul id="context-menu">
  ${self.context_menu_items()}
</ul>

<p>You are about to delete the following ${model_title} record:</p>

<div class="form-wrapper">
  ${form.render()|n}
</div><!-- form-wrapper -->

${self.confirmation()}
